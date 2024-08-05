import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.general_exception import GeneralException


@pytest.mark.crl_tst2  # Only applicable for Coral
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1234459_Verify_Next_Races_Module(BaseRacing):
    """
    TR_ID: C1234459
    NAME: Verify 'Next Races' Module
    DESCRIPTION: This test case is checking the UI of  'Next Races' module for Greyhounds.
    PRECONDITIONS: Make sure events are available for current day.
    """
    keep_browser_open = True

    def check_next_races_module_presence(self, is_present=True):
        self.site.wait_content_state(state_name='Greyhoundracing', timeout=5, raise_exceptions=False)
        try:
            sections = self.page_content.tab_content.accordions_list.items_as_ordered_dict
        except GeneralException:
            sections = {}
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
        self.__class__.today = vec.sb.SPORT_DAY_TABS.today
        self.__class__.tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
        self.__class__.future = vec.sb.SPORT_DAY_TABS.future

        if tests.settings.cms_env != 'prd0':
            self.setup_cms_next_races_number_of_events()
        self.__class__.is_desktop = False if self.device_type == 'mobile' else True
        next_races_toggle_config = self.get_initial_data_system_configuration().get('NextRacesToggle')
        if not next_races_toggle_config:
            next_races_toggle_config = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle_config.get('nextRacesComponentEnabled'):
            raise CmsClientException('Next Races component disabled in CMS')
        self.__class__.next_races_selections_number = self.get_greyhound_next_races_selections_number_from_cms()
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=10)
            self.ob_config.add_racing_specials_event(number_of_runners=2, ew_terms=self.ew_terms,
                                                     lp_prices={0: '1/4', 1: '7/1'}, time_to_start=10)
            self.__class__.event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern}'.upper()

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded.
        """
        self.site.wait_content_state(state_name='HomePage')

    def test_002_on_homepage_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On homepage tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

    def test_003_check_next_races_module(self):
        """
        DESCRIPTION: Check 'Next Races' module
        EXPECTED: For **Mobile and Tablet** , 'Next Races' module is displayed below 'Today's' tab> 'By meeting' switcher
        EXPECTED: For **Desktop** :
        EXPECTED: - for screen width > 970 px, 1025px, Next Races module is shown in line with Races Grids in main display area
        EXPECTED: - for screen width 1280px, 1600px, Next Races module is displayed on the second column of the display area
        """
        self.__class__.page_content = self.site.greyhound
        self.check_next_races_module_presence()

    def test_004_check_horizontal_scrolling_through_events(self):
        """
        DESCRIPTION: Check horizontal scrolling through events
        EXPECTED: For **Mobile and Tablet**:
        EXPECTED: 1. It is possible to move between events using swiping on Mobile/Tablet
        EXPECTED: 2. Swiping is fulfilled fluently
        EXPECTED: 3. The previous race is not shown when user swipes across the 'Next Races' module
        EXPECTED: 4. The next race is shown when user swipes across the 'Next Races' module
        EXPECTED: For **Desktop** :
        EXPECTED: 1. Clickable Rollover right arrow which appear on hover is displayed when content is more than one slide
        EXPECTED: 2. Clickable Rollover left arrow (content on both sides) which appear on hover is displayed when viewing slide 2 or more
        EXPECTED: 3. User can click both arrows to move content left and right
        """
        self.__class__.next_races = self.next_races_section.items_as_ordered_dict
        self.assertTrue(self.next_races, msg='No one race found in Next Race section')
        self.__class__.next_races_content = list(self.next_races.keys())
        list(self.next_races.values())[0].scroll_to()
        for i, (race_name, race) in enumerate(self.next_races.items()):
            if self.is_desktop:
                self.assertTrue(race.is_displayed(scroll_to=False),
                                msg=f'Next race: "{race_name}" not displayed after scrolling to')
                if i > 0 and i % 2 != 0:
                    self.next_races_section.click_next_arrow()
            else:
                race.scroll_to()
                self.assertTrue(race.is_displayed(),
                                msg=f'Next race: "{race_name}" not displayed after scrolling to')
                if i > 1:
                    prev_race_name, prev_race = list(self.next_races.items())[i - 2]
                    self.assertFalse(prev_race.is_displayed(expected_result=False, scroll_to=False),
                                     msg=f'Previous race: "{prev_race_name}" still displayed after scrolling to next')

        for i, (race_name, race) in enumerate(list(self.next_races.items())[::-1]):
            if self.is_desktop:
                if i % 2 == 0:
                    self.next_races_section.click_prev_arrow()
                    # need to add small sleep to make test run more stable after click with java script
                    self.device.driver.implicitly_wait(1)
                self.assertTrue(race.is_displayed(scroll_to=False),
                                msg=f'Previous race: "{race_name}" not displayed after scrolling to')
            else:
                race.scroll_to()
                self.assertTrue(race.is_displayed(),
                                msg=f'Previous race: "{race_name}" not displayed after scrolling to')
                if 1 < i < (len(self.next_races.items()) - 2):
                    next_race_name, next_race = list(self.next_races.items())[::-1][i - 3]
                    self.assertFalse(next_race.is_displayed(expected_result=False, scroll_to=False),
                                     msg=f'Next race: "{next_race_name}" still displayed after scrolling to previous')
        self.device.driver.implicitly_wait(0)

    def test_005_expand_next_races_module_and_check_default_quantity_of_eventsqayntity_of_the_events_sets_in_the_cms_cms___systemconfiguration__greyhoundnextraces___numberofevents(self):
        """
        DESCRIPTION: Expand 'Next Races' module and check default quantity of events
        DESCRIPTION: Qayntity of the events sets in the CMS (CMS -> systemConfiguration ->GreyhoundNextRaces -> numberOfEvents)
        EXPECTED: 1.  The 'Next Races' events to start are shown
        EXPECTED: 2.  Suspended events are not shown in 'Next Races' module
        EXPECTED: 3. Appropriate number of events (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: 4.  If number of selections is less than was set in CMS -> display the remaining selections
        EXPECTED: 5.  If there are no events to show -'Next Races' module is absent
        """
        next_races = self.get_next_races_section()
        group_header = next_races.group_header
        group_header.click()
        self.assertFalse(next_races.is_expanded(expected_result=False, timeout=3),
                         msg='Next Races module do not collapse after tapping on accordion header')
        group_header.click()
        self.assertTrue(next_races.is_expanded(),
                        msg='Next Races module do not expand after tapping on accordion header')
        sections = self.page_content.tab_content.accordions_list.items_as_ordered_dict
        next_races_section = sections.get(self.next_races_title, None)
        next_races = next_races_section.items_as_ordered_dict
        self.assertTrue(next_races, msg='No one race found in Next Race section')
        self.check_event_section()

    def test_006_verify_event_sectionsqayntity_of_the_events_sets_in_the_cms_cms___systemconfiguration__greyhoundnextraces___numberofselections(self):
        """
        DESCRIPTION: Verify event sections
        DESCRIPTION: Qayntity of the events sets in the CMS (CMS -> systemConfiguration ->GreyhoundNextRaces -> numberOfSelections)
        EXPECTED: -Appropriate number of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: - If number of selections is less than was set in CMS -> display the remaining selections
        EXPECTED: - 'Unnamed Favourite' runner shouldn't be shown on the 'Next Races' module
        """
        # Covered in step#5

    def test_007_verify_full_race_card_link(self):
        """
        DESCRIPTION: Verify 'FULL RACE CARD' link
        EXPECTED: Link is shown under the selections
        """
        for race_name, race in self.next_races.items():
            self.assertTrue(race.has_view_full_race_card(),
                            msg=f'"Full Race Card" not found for race: "{race_name}"')

    def test_008_click_by_time_switcher(self, tab=None):
        """
        DESCRIPTION: Click 'By Time' switcher
        EXPECTED: For **Mobile and Tablet** , 'Next Races' module is displayed below 'Today's' tab> 'By Time' switcher
        EXPECTED: For **Desktop** :
        EXPECTED: - for screen width > 970 px, 1025px, Next Races module is shown in line with Races Grids in main display area
        EXPECTED: - for screen width 1280px, 1600px, Next Races module is displayed on the second column of the display area
        """
        tab = self.today if not tab else tab
        self.site.greyhound.tabs_menu.click_button(tab)
        self.assertEqual(self.site.greyhound.tabs_menu.current, tab,
                         msg=f'Opened grouping button "{self.site.greyhound.tabs_menu.current}" '
                             f'is not the same as expected "{tab}"')
        #OZONE-3455-----Q4-Coral Greyhounds: Remove By Time and By Meeting tabs
        # if self.device_type == 'desktop':
        #     self.site.greyhound.tab_content.grouping_buttons.click_button(
        #         vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING)
        #     self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
        #                      vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING,
        #                      msg=f'Opened tab "{self.site.greyhound.tab_content.current}" is not '
        #                          f'the same as expected "{vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING}"')

    def test_009_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps #4-7
        EXPECTED: Results are the same
        """
        self.test_004_check_horizontal_scrolling_through_events()
        self.test_005_expand_next_races_module_and_check_default_quantity_of_eventsqayntity_of_the_events_sets_in_the_cms_cms___systemconfiguration__greyhoundnextraces___numberofevents()
        self.test_006_verify_event_sectionsqayntity_of_the_events_sets_in_the_cms_cms___systemconfiguration__greyhoundnextraces___numberofselections()
        self.test_007_verify_full_race_card_link()

    def test_010_go_to_tomorrow_tab_and_verify_next_races_module(self):
        """
        DESCRIPTION: Go to 'Tomorrow' tab and verify 'Next Races' module
        EXPECTED: 'Next Races' module is absent
        """
        self.test_008_click_by_time_switcher(tab=self.tomorrow)
        self.check_next_races_module_presence(is_present=False)

    def test_011_go_to_the_future_tab_and_verify_next_races_module(self):
        """
        DESCRIPTION: Go to the 'Future' tab and verify 'Next Races' module
        EXPECTED: 'Next Races' module is absent
        """
        self.test_008_click_by_time_switcher(tab=self.future)
        self.check_next_races_module_presence(is_present=False)
