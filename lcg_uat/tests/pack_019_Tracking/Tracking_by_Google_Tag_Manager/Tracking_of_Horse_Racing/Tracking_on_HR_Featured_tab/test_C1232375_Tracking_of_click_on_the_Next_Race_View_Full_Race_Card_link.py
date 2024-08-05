import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.google_analytics
@pytest.mark.other
@pytest.mark.next_races
@pytest.mark.low
@vtest
class Test_C1232375_C1232380_Tracking_of_click_on_the_Next_Race_View_Full_Race_Card_link(BaseRacing, BaseDataLayerTest):
    """
    TR_ID: C1232375
    TR_ID: C1232380
    VOL_ID: C9697905
    NAME: Tracking of click on the Next Race View Full Race Card link
    PRECONDITIONS: Horse Racing landing page is opened.
    PRECONDITIONS: Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: Browser console should be opened
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event_params = self.ob_config.add_UK_racing_event(time_to_start=10, number_of_runners=1, lp_prices={0: '3/5'})
        event_off_time = event_params.event_off_time
        self.__class__.event_name = f'{event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'

    def test_001_navigate_to_horse_racing(self):
        """
        DESCRIPTION: Navigate to HR -> Featured tab
        """
        self.navigate_to_page(name='horse-racing')

        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab "%s" is not the same as expected %s'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))

        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Can not find any section')

    def test_002_scroll_till_next_races_module_and_collapse_it(self):
        """
        DESCRIPTION: Scroll till Next Races module and collapse it.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'next 4 races',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        next_races = self.next_races_title
        self.__class__.next_races_section = self.sections.get(next_races)
        self.assertTrue(self.next_races_section, msg='Can not find section: "%s"' % next_races)
        self.next_races_section.collapse()
        self.assertFalse(self.next_races_section.is_expanded(expected_result=False),
                         msg='Section "%s" is expanded' % self.uk_and_ire_type_name)

        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='collapse')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': 'next 4 races',
                             'eventLabel': 'collapse'
                             }
        self.compare_json_response(actual_response, expected_response)
        self.next_races_section.expand()
        self.assertTrue(self.next_races_section.is_expanded(), msg='Section "%s" is not expanded' % self.uk_and_ire_type_name)

    def test_003_scroll_till_next_races_module_click_on_view_full_race_card(self):
        """
        DESCRIPTION: Scroll till Next Races module. Click on "View Full Race Card" link.
        DESCRIPTION: Type in browser console "dataLayer" and press "Enter"
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'next 4 races',
        EXPECTED: 'eventLabel' : 'full race card'
        EXPECTED: })
        """
        events = self.next_races_section.items_as_ordered_dict
        self.assertTrue(events, msg='Can not find event')
        autotest_event = events.get(self.event_name)
        self.assertTrue(autotest_event, msg='Event "%s" was not found' % self.event_name)
        autotest_event.click()

        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='next 4 races')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'horse racing',
                             'eventAction': 'next 4 races',
                             'eventLabel': 'full race card'
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_004_navigate_to_the_different_page_and_come_back_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to the different page and come back to Horse Racing landing page.
        DESCRIPTION: Collapse the Next Race module, Type in browser console "dataLayer" and press "Enter".
        EXPECTED: One more event with the following details has been created in the data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'horse racing',
        EXPECTED: 'eventAction' : 'next 4 races',
        EXPECTED: 'eventLabel' : 'collapse'
        EXPECTED: })
        """
        self.test_001_navigate_to_horse_racing()
        self.test_002_scroll_till_next_races_module_and_collapse_it()
        self.test_003_scroll_till_next_races_module_click_on_view_full_race_card()
