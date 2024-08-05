from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.high
@pytest.mark.user_journey_next_horse_race
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.cms
@pytest.mark.next_races
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C1108079_Verify_Next_Races_Module(BaseRacing):
    """
    TR_ID: C1108079
    NAME: Verify 'Next Races' Module
    """
    keep_browser_open = True
    page_content = None

    def check_next_races_module_presence(self, is_present=True):
        self.site.wait_content_state(state_name='Horseracing', timeout=5, raise_exceptions=False)
        sections = self.page_content.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.next_races_section = sections.get(self.next_races_title, None)
        self.assertIs(bool(self.next_races_section), is_present,
                      msg=f'Section: "{self.next_races_title}" is presence status: '
                          f'"{bool(self.next_races_section)}", expected: "{is_present}"')

    def check_event_section(self):
        self.__class__.next_races = self.next_races_section.items_as_ordered_dict
        self.assertTrue(self.next_races, msg='No one race found in Next Race section')
        for race_name, race in self.next_races.items():
            race.scroll_to()
            selections = race.items_as_ordered_dict
            self.assertTrue(selections, msg=f'No one selection found for race: "{race_name}"')
            self.assertLessEqual(len(selections), self.next_races_selections_number,
                                 msg=f'Actual race: "{race_name}" selections number: "{len(selections)}", '
                                     f'expected less or equals than CMS configured: '
                                     f'"{self.next_races_selections_number}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Next4 event
        EXPECTED: Next4 event is created
        """
        if tests.settings.cms_env != 'prd0':
            self.setup_cms_next_races_number_of_events()
        self.__class__.is_desktop = False if self.device_type == 'mobile' else True
        next_races_toggle_config = self.get_initial_data_system_configuration().get('NextRacesToggle')
        if not next_races_toggle_config:
            next_races_toggle_config = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle_config.get('nextRacesComponentEnabled'):
            raise CmsClientException('Next Races component disabled in CMS')

        if tests.settings.cms_env != 'prd0':
            self.setup_cms_next_races_number_of_events()
        self.__class__.is_desktop = False if self.device_type == 'mobile' else True
        self.__class__.next_races_selections_number = self.get_next_races_selections_number_from_cms()
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=10)
            self.ob_config.add_racing_specials_event(number_of_runners=2, ew_terms=self.ew_terms,
                                                     lp_prices={0: '1/4', 1: '7/1'}, time_to_start=10)

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: Horse Racing Landing page is opened by default on 'Featured' tab
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as '
                             f'expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

    def test_002_check_next_races_module(self):
        """
        DESCRIPTION: Check 'Next Races' module
        EXPECTED: For Mobile and Tablet:
        EXPECTED:  - 'Next Races' module is displayed below 'Today's enhanced Races' module (if available)
        EXPECTED: For Desktop:
        EXPECTED:  - Next Races module is shown in line with Races Grids in main display area
        """
        self.__class__.page_content = self.site.horse_racing
        self.check_next_races_module_presence()

    def test_003_check_horizontal_scrolling_navigation_arrows_through_events(self):
        """
        DESCRIPTION: Check Horizontal scrolling/Navigation arrows through events
        EXPECTED: For Mobile and Tablet:
        EXPECTED:  - It is possible to move between events using swiping on Mobile/Tablet
        EXPECTED:  - Swiping is fulfilled fluently
        EXPECTED:  - The previous race is not shown when user swipes across the 'Next Races' module
        EXPECTED:  - The next race is shown when user swipes across the 'Next Races' module
        EXPECTED: For Desktop:
        EXPECTED:  - Clickable Navigation right arrow which appear on hover is displayed when content is more than one slide
        EXPECTED:  - Clickable Navigation left arrow (content on both sides) which appear on hover is displayed when viewing slide 2 or more
        EXPECTED:  - User can click both arrows to move content left and right
        """
        self.__class__.next_races = self.next_races_section.items_as_ordered_dict
        self.assertTrue(self.next_races, msg='No one race found in Next Race section')
        self.__class__.next_races_content = list(self.next_races.keys())
        # need scroll to first race section to correct perform next validations
        list(self.next_races.values())[0].scroll_to()
        for i, (race_name, race) in enumerate(self.next_races.items()):
            if self.is_desktop:
                if i > 0 and i % 2 != 0:
                    self.next_races_section.click_next_arrow()
                # need to add small sleep to make test run more stable after click with java script
                self.device.driver.implicitly_wait(1)
                next_race_name, next_race = list(
                    self.next_races.items())[i + 1] if i < (len(self.next_races.items()) - 1) else (race_name, race)
                self.assertTrue(next_race.is_displayed(scroll_to=False),
                                msg=f'Next race: "{next_race_name}" not displayed after scrolling to')
            else:
                race.scroll_to()
                self.assertTrue(race.is_displayed(),
                                msg=f'Next race: "{race_name}" not displayed after scrolling to')

            if i > 1:
                prev_race_name, prev_race = list(self.next_races.items())[i - 2]
                self.assertFalse(prev_race.is_displayed(expected_result=False, scroll_to=False),
                                 msg=f'Previous race: "{prev_race_name}" still displayed after scrolling to next')
        # need scroll to last race section to correct perform next validations
        list(self.next_races.values())[-1].scroll_to()
        for i, (race_name, race) in enumerate(list(self.next_races.items())[::-1]):
            if self.is_desktop:
                if i % 2 == 0:
                    self.next_races_section.click_prev_arrow()
                # need to add small sleep to make test run more stable after click with java script
                self.device.driver.implicitly_wait(1)
                prev_race_name, prev_race = list(
                    self.next_races.items())[::-1][i + 1] if i < (len(self.next_races.items()) - 1) else \
                    (race_name, race)
                self.assertTrue(prev_race.is_displayed(scroll_to=False),
                                msg=f'Previous race: "{prev_race_name}" not displayed after scrolling to')
            else:
                race.scroll_to()
                self.assertTrue(race.is_displayed(),
                                msg=f'Previous race: "{race_name}" not displayed after scrolling to')
            if 1 < i < (len(self.next_races.items()) - 2):
                next_race_name, next_race = list(self.next_races.items())[::-1][i - 3]
                self.assertFalse(next_race.is_displayed(expected_result=False, scroll_to=False),
                                 msg=f'Next race: "{next_race_name}" still displayed after scrolling to previous')


    def test_004_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: Default number of selections is 3. (*It is a CMS controlled value)
        EXPECTED: If number of selections is less than 3 -> display the remaining selections
        """
        sections = self.page_content.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.next_races_section = sections.get(self.next_races_title, None)
        self.__class__.next_races = self.next_races_section.items_as_ordered_dict
        self.assertTrue(self.next_races, msg='No one race found in Next Race section')
        self.check_event_section()

    def test_005_verify_full_race_card_link(self):
        """
        DESCRIPTION: Verify 'Full Race Card' link
        EXPECTED: Link is shown under the selections and links to EDP of respective event
        """
        for race_name, race in self.next_races.items():
            self.assertTrue(race.has_view_full_race_card(),
                            msg=f'"Full Race Card" not found for race: "{race_name}"')

    def test_006_go_to_another_tab_and_verify_next_races_module(self, tab_name=vec.racing.RACING_FUTURE_TAB_NAME):
        """
        DESCRIPTION: Go to the 'Antepost' tab and Verify 'Next Races' module
        EXPECTED: 'Next Races' module is absent
        """
        result = self.page_content.tabs_menu.click_button(tab_name)
        self.assertTrue(result, msg=f'"{tab_name}" tab not opened')
        self.check_next_races_module_presence(is_present=False)

    def test_007_repeat_step_6_for_specials_yourcall_tab(self):
        """
        DESCRIPTION: Repeat step #6 for 'Specials', 'YourCall' tab
        """
        self.test_006_go_to_another_tab_and_verify_next_races_module(tab_name=vec.racing.RACING_SPECIALS_TAB_NAME)
        # this step is no longer valid
        # if self.brand != 'ladbrokes':
        #     self.test_006_go_to_another_tab_and_verify_next_races_module(tab_name=vec.racing.RACING_YOURCALL_TAB_NAME)

    def test_008_navigate_to_the_homepage_next_races(self):
        """
        DESCRIPTION: Navigate to the homepage > 'Next Races'
        EXPECTED: 'Next Races' tab content is the same as 'Next Races' module
        EXPECTED: For Desktop:
        EXPECTED:  - Link is shown under the module on the bottom right side and it redirected user to the 'Horse Racing' Landing page
        """
        self.site.go_to_home_page()
        self.__class__.page_content = self.site.home
        module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races)
        self.__class__.next_races_section = \
            self.site.home.get_module_content(module_name=module_name).accordions_list
        self.assertTrue(self.next_races_section, msg=f'"{self.next_races_title}" not found on Home page')
        self.assertTrue(self.next_races, msg=f'No one race found in section: "{self.next_races_title}"')
        self.assertListEqual(list(self.next_races.keys()), self.next_races_content,
                             msg=f'Actual section: "{self.next_races_title}" '
                                 f'content: \n{list(self.next_races.keys())}\n Expected: '
                                 f'\n{self.next_races_content}')
        if self.is_desktop:
            self.assertTrue(self.next_races_section.has_show_more_link(),
                            msg=f'Link not found under the: "{self.next_races_title}" module')
            self.next_races_section.show_more_link.click()
            self.site.wait_content_state(state_name='HorseRacing')
            wait_for_haul(5)
            self.site.horse_racing.header_line.back_button.click()
            self.site.wait_content_state(state_name='HomePage')
            self.__class__.next_races_section = \
                self.site.home.get_module_content(module_name=module_name).accordions_list
            self.assertTrue(self.next_races_section, msg=f'"{self.next_races_title}" not found on Home page')

    def test_009_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps # 4-6
        """
        if self.device_type == 'desktop':
            self.check_event_section()
        else:
            self.__class__.next_races = self.next_races_section.items_as_ordered_dict
            self.assertTrue(self.next_races, msg='No one race found in Next Race section')
        self.test_005_verify_full_race_card_link()
        if not self.is_desktop:
            self.page_content.tabs_menu.click_button('IN-PLAY')
            result = wait_for_result(lambda: self.page_content.tabs_menu.current == 'IN-PLAY',
                                     name='Tab "IN-PLAY" to become active',
                                     bypass_exceptions=StaleElementReferenceException,
                                     timeout=3)
            current_tab = self.page_content.tabs_menu.current
            self.assertTrue(result, msg=f'"IN-PLAY" tab  is not active, active is "{current_tab}"')
            self.check_next_races_module_presence(is_present=False)
