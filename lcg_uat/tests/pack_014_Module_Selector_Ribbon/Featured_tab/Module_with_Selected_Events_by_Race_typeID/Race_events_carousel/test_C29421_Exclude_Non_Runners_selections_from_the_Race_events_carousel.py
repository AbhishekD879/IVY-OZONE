import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C29421_Exclude_Non_Runners_selections_from_the_Race_events_carousel(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C29421
    NAME: Exclude Non-Runners selections from the <Race> events carousel
    DESCRIPTION: This test case verifies how 'Non-Runners' will be excluded from the <Race> events carousel
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on outcome level to see horse name
    PRECONDITIONS: **'outcomeStatusCode' **to see outcome status
    PRECONDITIONS: 'Non-Runners' is a selection which contains **'N/R'** text next to it's name
    PRECONDITIONS: All those selections should be suspended 'outcomeStatusCode'='S'
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True
    selection_ids_1 = []
    selection_ids_2 = []
    race_name = []
    selection_name = []

    def create_events(self, number_of_runners):
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=number_of_runners, time_to_start=3)
        race_name = event_params.ss_response['event']['name']
        self.race_name.append(race_name if tests.settings.brand == 'bma' else race_name.upper())
        self.selection_ids_1.extend(list(event_params.selection_ids.keys())) if number_of_runners == 5 \
            else self.selection_ids_2.extend(list(event_params.selection_ids.keys()))
        event_id = event_params.event_id
        event_off_time = event_params.event_off_time
        name = self.horseracing_autotest_uk_name_pattern if self.brand == 'bma' and self.device_type == 'desktop' else \
            self.horseracing_autotest_uk_name_pattern.upper()
        self.__class__.created_event_name = f'{event_off_time} {name}'
        win_or_each_way_market_id = event_params.market_id

        selection_name, selection_id = list(event_params.selection_ids.items())[0]
        self.selection_name.append(selection_name)
        new_selection_name = f'{selection_name} N/R'

        self.ob_config.change_selection_name(selection_id=selection_id, new_selection_name=new_selection_name)
        self.ob_config.result_selection(selection_id=selection_id, market_id=win_or_each_way_market_id,
                                        event_id=event_id, result='V')
        self.ob_config.confirm_result(selection_id=selection_id, market_id=win_or_each_way_market_id,
                                      event_id=event_id, result='V')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Non-Runners
        """
        # This cms switcher added to display all events, not only with LP prices
        self.cms_config.next_races_price_switcher(show_priced_only=False)
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)
        self.create_events(number_of_runners=5)
        self.create_events(number_of_runners=2)
        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id
        self.__class__.is_executed_on_desktop = self.device_type in ['desktop']
        self.__class__.featured_module_name = \
            self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId', id=race_type_id,
                                                    module_time_from_hours_delta=-10,
                                                    events_time_from_hours_delta=-10,
                                                    max_rows=self.max_number_of_events)['title'].upper()

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED:
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.featured_module_name)

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: 1.  'Feature' tab is selected by default
        EXPECTED: 2.  Module created by <Race> type ID is shown
        """
        if not self.is_executed_on_desktop:
            featured_module = \
                self.site.home.get_module_content(
                    self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

            self.__class__.section = \
                featured_module.accordions_list.items_as_ordered_dict.get(self.featured_module_name)
            self.assertTrue(self.section, msg=f'Section "{self.featured_module_name}" is not found on FEATURED tab')

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        if self.is_executed_on_desktop:
            featured_module = self.site.home.desktop_modules.featured_module
            self.assertTrue(featured_module, msg='"Featured" module is not displayed')

            featured_content = featured_module.tab_content
            featured_modules = featured_content.accordions_list.items_as_ordered_dict.keys()
            self.assertTrue(featured_content.accordions_list, msg='"Featured" module does not contain any accordions')
            self.assertIn(self.featured_module_name, featured_content.accordions_list.items_as_ordered_dict.keys(),
                          msg=f'Module "{self.featured_module_name}" is not displayed. '
                              f'Please check list of all displayed modules:\n"{featured_modules}"')

            self.__class__.section = featured_content.accordions_list.items_as_ordered_dict[self.featured_module_name]
            self.assertTrue(self.section, msg='No accordions displayed in "Featured" section on Home page')

    def test_004_on_the_race_events_carousel_find_an_event_which_contains_non_runner_selection(self):
        """
        DESCRIPTION: On the <Race> events carousel find an event which contains 'non-runner' selection
        EXPECTED: Event is displayed in the <Race> events carousel
        """
        self.assertGreater(len(self.selection_ids_1), 3,
                           msg=f'Actual number of selections :"{len(self.selection_ids_1)}" is not greater than'
                               f'Expected number of selections :"{3}"')

    def test_005_verify_selections_in_the_event(self):
        """
        DESCRIPTION: Verify selections in the event
        EXPECTED: 1.  'Non-Runners' won't appear in the <Race> events carousel
        EXPECTED: 2.  'Non-Runners' are excluded by **outcomeStatusCode **attribute (suspended selections are not shown in the <Race> events carousel )
        """
        event = self.section.items_as_ordered_dict.get(self.race_name[0])
        selections = event.items_names
        self.assertNotIn(self.selection_name[0], selections,
                         msg=f'Non runner Selection: "{self.selection_name[0]}" '
                             f'is available in module event: "{self.race_name[0]}"')

    def test_006_find_an_event_which_contains_3_or_less_selection_and_one_of_those_selections_is_non_runners(self):
        """
        DESCRIPTION: Find an event which contains 3 or less selection and one of those selections is 'non-runners'
        EXPECTED: Event is shown
        """
        self.assertLessEqual(len(self.selection_ids_2), 3,
                             msg=f'Actual number of selections :"{len(self.selection_ids_2)}" is not same as'
                                 f'Expected number of selections :"{3}"')

    def test_007_verify_selections_in_the_race_events_carousel(self):
        """
        DESCRIPTION: Verify selections in the <Race> events carousel
        EXPECTED: 'Non- Runner' selections still are not displayed
        """
        event = self.section.items_as_ordered_dict.get(self.race_name[1])
        selections = event.items_names
        self.assertNotIn(self.selection_name[1], selections,
                         msg=f'Non runner Selection: "{self.selection_name[1]}" '
                             f'is available in module event: "{self.race_name[1]}"')