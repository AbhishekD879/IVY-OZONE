import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.homepage_featured
@vtest
class Test_C29419_Verify_Excluding_Unnamed_Favourite_Selections_from_the_Race_events_carousel(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C29419
    NAME: Verify Excluding 'Unnamed Favourite' Selections from the <Race> events carousel
    DESCRIPTION: This test case verifies 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selections excluding from the displaying within <Race> events carousel within modules created by <Race> typeID.
    DESCRIPTION: **Jira tickets:** BMA-6571 CMS: Featured Tab Module - Horse Racing
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day which contain 'Unnamed Favorite' and 'Unnamed 2nd Favorite' selections with 'selection type'='Unnamed Favorite/Unnamed 2nd Favorite' set on selection level in TI tool
    PRECONDITIONS: 3) In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Events
        """
        self.__class__.event_info = self.ob_config.add_UK_racing_event(number_of_runners=1, unnamed_favorites=True)
        self.__class__.race_name = self.event_info.ss_response['event']['name']
        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id
        self.__class__.is_executed_on_desktop = self.device_type in ['desktop']
        self.__class__.featured_module_name = \
            self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId', id=race_type_id,
                                                    module_time_from_hours_delta=-10,
                                                    events_time_from_hours_delta=-10,
                                                    max_rows=self.max_number_of_events)['title'].upper()

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.featured_module_name)

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by <Race> type ID is shown
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

    def test_004_pick_event_from_race_module___remove_all_but_one_selections_fromwin_or_each_way_marketmake_sure_two_unnamed_favourite_selections_are_also_remain(self):
        """
        DESCRIPTION: Pick event from <Race> module -> Remove all but one selections from 'Win or Each Way' market
        DESCRIPTION: Make sure two 'Unnamed Favourite' selections are also remain
        EXPECTED: Only three selections are available for the Win or Each Way market
        """
        selections = list(self.event_info.selection_ids)
        self.assertEqual(len(selections), 3,
                         msg=f'Actual number of selections :"{len(selections)}" is not same as'
                             f'Expected number of selections :"{3}"')
        self.assertIn(vec.racing.UNNAMED_FAVORITE, selections,
                      msg=f'Selection: "{vec.racing.UNNAMED_FAVORITE}" '
                          f'is not available in module event: "{self.race_name}"')
        self.assertIn(vec.racing.UNNAMED_FAVORITE_2ND, selections,
                      msg=f'Selection: "{vec.racing.UNNAMED_FAVORITE_2ND}" '
                          f'is not available in module event: "{self.race_name}"')

    def test_005_go_to_the_invictus_application_and_check_the_event_in_the_verified_module_created_by_race_typeid(self):
        """
        DESCRIPTION: Go to the Invictus application and check the event in the verified module created by <Race> typeID
        EXPECTED: Only one selection is shown for this event
        EXPECTED: 'Unnamed Favourite' selections are excluded from the module created by <Race> typeID
        """
        race_name = self.race_name if tests.settings.brand == 'bma' else self.race_name.upper()
        event = self.section.items_as_ordered_dict.get(race_name)
        selections = event.items_names
        self.assertNotIn(vec.racing.UNNAMED_FAVORITE, selections,
                         msg=f'Selection: "{vec.racing.UNNAMED_FAVORITE}" '
                             f'is available in module event: "{self.race_name}"')
        self.assertNotIn(vec.racing.UNNAMED_FAVORITE_2ND, selections,
                         msg=f'Selection: "{vec.racing.UNNAMED_FAVORITE_2ND}" '
                             f'is available in module event: "{self.race_name}"')
