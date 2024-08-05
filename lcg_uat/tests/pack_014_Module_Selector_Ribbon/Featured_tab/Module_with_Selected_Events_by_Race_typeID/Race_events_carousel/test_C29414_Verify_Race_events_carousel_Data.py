from collections import OrderedDict

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.module_ribbon
@pytest.mark.smoke
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.high
@vtest
class Test_C29414_Verify_Race_events_carousel_Data(BaseFeaturedTest, BaseRacing, BaseSportTest):
    """
    TR_ID: C29414
    NAME: Verify <Race> events carousel Data
    DESCRIPTION: This test case is for checking a data which is displayed in <Race> events carousel of module created by <Race> type ID within Featured tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
        DESCRIPTION: 2) Make sure events are available within module created by <Race> type ID for current day
        DESCRIPTION: 3) In order to check event data use link:
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
        DESCRIPTION: *   XXX - event ID
        DESCRIPTION: *   X.XX - current supported version of OpenBet release
        DESCRIPTION: *   LL - language (e.g. en, ukr)
        DESCRIPTION: See attributes:
        DESCRIPTION: - **'name'** to check an event name and local time
        DESCRIPTION: - **'typeFlagCodes' **to check event group
        DESCRIPTION: - **'eventStatusCode'** to check whether event is active or suspended
        DESCRIPTION: - **'marketStatusCode' **to see market status
        DESCRIPTION: - **'outcomeStatusCode'** to see outcome status
        DESCRIPTION: 4) Invictus application is loaded
        DESCRIPTION: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be 
        DESCRIPTION: delay up to 5-10 mins before they will be applied and visible on the front end.
        """
        event_1 = self.ob_config.add_UK_racing_event(number_of_runners=2)
        event_2 = self.ob_config.add_UK_racing_event(number_of_runners=2)
        event_3 = self.ob_config.add_UK_racing_event(hours=22)
        event_4 = self.ob_config.add_UK_racing_event(number_of_runners=2)

        self.__class__.event_1_ID = event_1.event_id
        self.__class__.event_2_ID = event_2.event_id
        self.__class__.event_3_ID = event_3.event_id
        self.__class__.event_4_ID = event_4.event_id

        self.__class__.event_1_name = f'{event_1.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_2_name = f'{event_2.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_3_name = f'{event_3.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_4_name = f'{event_4.event_off_time} {self.horseracing_autotest_uk_name_pattern}'

        self.__class__.events = {self.event_1_ID: self.event_1_name, self.event_2_ID: self.event_2_name,
                                 self.event_3_ID: self.event_3_name, self.event_4_ID: self.event_4_name}

        self.__class__.events_date_time = {event_1.event_date_time: self.event_1_name,
                                           event_2.event_date_time: self.event_2_name,
                                           event_3.event_date_time: self.event_3_name,
                                           event_4.event_date_time: self.event_4_name}

        selections_ids = list(event_4.selection_ids.values())

        self.__class__.market_ID = event_1.market_id
        self.__class__.selection_name = list(event_4.selection_ids.keys())[0]
        self.__class__.type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.type_id, show_all_events=True)['title'].upper()

        self.ob_config.change_market_state(event_id=self.event_1_ID, market_id=self.market_ID, displayed=True, active=False)
        self.ob_config.change_event_state(event_id=self.event_2_ID, displayed=True, active=False)
        self.ob_config.change_selection_state(selection_id=selections_ids[-1], displayed=True, active=False)

        self.site.wait_content_state(state_name='HomePage')
        self.wait_for_featured_module(name=self.module_name)

    def test_001_for_mobile_tablet_go_to_module_selector_ribbon_module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: 'Feature' tab is selected by default
        EXPECTED: Module created by <Race> type ID is shown
        """
        if self.device_type == 'mobile':
            home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

            selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(selected_tab, home_featured_tab_name,
                             msg=f'Selected tab is "{selected_tab}" instead of "{home_featured_tab_name}" tab')

            self.__class__.module = self.get_section(self.module_name)
            self.assertTrue(self.module, msg='No accordions displayed in "Featured" tab on Home page')

    def test_002_for_desktop_scroll_the_page_down_to_featured_section_module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel,
        EXPECTED: In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: Module created by <Race> type ID is shown
        """
        if self.device_type == 'desktop':
            featured_module = self.site.home.desktop_modules.featured_module
            self.assertTrue(featured_module, msg='"Featured" module is not displayed')

            featured_content = featured_module.tab_content
            featured_modules = featured_content.accordions_list.items_as_ordered_dict.keys()
            self.assertTrue(featured_content.accordions_list, msg='"Featured" module does not contain any accordions')
            self.assertIn(self.module_name, featured_content.accordions_list.items_as_ordered_dict.keys(),
                          msg=f'Module "{self.module_name}" is not displayed. '
                          f'Please check list of all displayed modules:\n"{featured_modules}"')

            self.__class__.module = featured_content.accordions_list.items_as_ordered_dict[self.module_name]
            self.assertTrue(self.module, msg='No accordions displayed in "Featured" section on Home page')

    def test_003_check_race_events_carousel_within_verified_module(self):
        """
        DESCRIPTION: Check <Race> events carousel within verified module
        EXPECTED: <Race> events carousel is displayed below the module header
        """
        self.__class__.displayed_events = self.module.items_as_ordered_dict
        self.assertTrue(self.displayed_events, msg=f'No events found in module "{self.module_name}"')

    def test_004_verify_data_in_race_events_carousel(self):
        """
        DESCRIPTION: Verify data in <Race> events carousel
        EXPECTED: - Races retrieved by typeID in CMS are shown
        EXPECTED: - Data corresponds to the Site Server response.
        EXPECTED: See attribute **'name'**.
        EXPECTED: - Events are sorted by **'start time'**: the first event to start is shown first.
        """
        for event_id in self.events.keys():
            query = self.ss_query_builder.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.ID, OPERATORS.EQUALS, event_id))
            filtered_ss_event = self.ss_req.ss_event_to_outcome_for_class(query_builder=query)
            self.assertTrue(filtered_ss_event, msg=f'Event "|{self.events[event_id]}|" with id "{event_id}" '
                            f'is not found in SS response.')

        displayed_events_order = list(self.displayed_events.keys())
        ordered_events = OrderedDict(sorted(self.events_date_time.items()))
        ordered_events_list = list(ordered_events.values())

        expected_events_order = [x for x in displayed_events_order if x in ordered_events_list]
        actual_events_order = [x for x in displayed_events_order if x in expected_events_order]

        self.assertListEqual(actual_events_order, expected_events_order,
                             msg=f'\nActual events order: \n"{actual_events_order}"'
                             f'\nis not as expected: \n"{expected_events_order}"')

    def test_005_verify_events_which_are_displayed_in_the_race_events_carousel(self):
        """
        DESCRIPTION: Verify events which are displayed in the <Race> events carousel
        EXPECTED: Only active events are displayed in the <Race> events carousel
        EXPECTED: (for those events attribute **'eventStatusCode'**='A' in the Site Server response)
        EXPECTED: Only events with active markets are shown in the <Race> events carousel (**'marketStatusCode'**='A')
        """
        if self.device_type == 'desktop':
            for key in self.events.keys():
                if self.brand == 'ladbrokes':
                    self.__class__.events[key] = self.events[key].upper()
                else:
                    self.__class__.events[key] = self.events[key]
        self.__class__.events_names = list(self.events.values())

        result = wait_for_result(lambda: self.events_names[0] not in self.displayed_events.keys(),
                                 name='Event to be undisplayed', timeout=3)
        self.assertTrue(result, msg=f'Event "{self.events_names[0]}" with inactive market should not be displayed')

        result = wait_for_result(lambda: self.events_names[1] not in self.displayed_events.keys(),
                                 name='Event to be undisplayed', timeout=3)
        self.assertTrue(result, msg=f'Inactive event "{self.events_names[1]}" should not be displayed')

    def test_006_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: 3 selections in the event are shown
        EXPECTED: Only active selections are shown (**'outcomeStatusCode'**='A')
        """
        result = wait_for_result(lambda: self.events_names[2] in self.displayed_events.keys(),
                                 name='Event to be displayed', timeout=3)
        self.assertTrue(result, msg=f'Event "{self.events_names[2]}" is not displayed')

        event = self.displayed_events[self.events_names[2]]
        selections = event.items_as_ordered_dict
        self.assertEqual(len(selections), 3, msg=f'Number of shown selections: {len(selections)} '
                         f'is not as expected: 3')

        result = wait_for_result(lambda: self.events_names[3] in self.displayed_events.keys(),
                                 name='Event to be displayed', timeout=3)
        self.assertTrue(result, msg=f'Event "{self.events_names[2]}" is not displayed')

        event = self.displayed_events[self.events_names[3]]
        selections = list(event.items_as_ordered_dict.keys())
        self.assertEqual(len(selections), 1, msg='Only active selections should be shown for the event')
        self.assertEqual(self.selection_name, selections[0], msg='Active selections should be shown for the event')
