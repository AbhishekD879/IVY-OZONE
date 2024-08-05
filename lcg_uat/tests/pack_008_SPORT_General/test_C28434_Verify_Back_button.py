import pytest
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.back_button
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.in_play
@pytest.mark.sports
@pytest.mark.safari
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-49471')
@vtest
class Test_C28434_Verify_Back_button(BaseSportTest, BaseRacing, BaseCashOutTest):
    """
    TR_ID: C28434
    NAME: Verify Back button
    DESCRIPTION: This test case verifies Back button functionality
    PRECONDITIONS: **JIRA ticket **: BMA-3547, BMA-4830
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football events for tst2
        """
        if tests.settings.backend_env != 'prod':
            self.create_several_autotest_premier_league_football_events(number_of_events=2)
            self.create_several_autotest_premier_league_football_events(number_of_events=2, is_live=True)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: *  'Matches' tab is opened by default
        """
        self.site.open_sport(name='FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current
        self.__class__.matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                  self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, self.matches_tab_name,
                         msg=f'Default tab is "{current_tab_name}", it is not "{self.matches_tab_name}"')

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event details page
        EXPECTED: Event details page is opened
        """
        event = self.get_event_from_league()
        event.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_004_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: User is directed to <Sport> Landing Page to the previously navigated tab
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Football')
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.matches_tab_name,
                         msg=f'Default tab is "{current_tab_name}", it is not "{self.matches_tab_name}"')

    def test_005_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Event Details page
        EXPECTED: Event Details page is opened
        """
        self.test_003_go_to_event_details_page()

    def test_006_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: User is directed to <Sport> Landing page irrespectively to the previously navigated tab
        """
        self.test_004_tap_back_button()

    def test_007_navigate_inside_sport_landing_page(self):
        """
        DESCRIPTION: Navigate inside <Sport> landing page
        EXPECTED: <Sport> Landing page is opened
        """
        if self.device_type == 'desktop':
            in_play_tab_name = self.expected_sport_tabs.in_play
            self.assertTrue(self.site.football.tabs_menu.click_button(in_play_tab_name),
                            msg=f'"{in_play_tab_name}" is not opened')
        else:
            if self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                   category_id=self.ob_config.football_config.category_id):
                in_play_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                           self.ob_config.football_config.category_id)
                open_in_play = self.site.football.tabs_menu.click_button(in_play_tab_name)
                self.assertTrue(open_in_play, msg=f'"{in_play_tab_name}" is not opened')
            else:
                self._logger.warning(f'*** "In Play" tab is not supposed to be present. '
                                     f'Probably it is disabled in CMS. Skipping verification of presence.')
        self.site.wait_content_state(state_name='Football')

    def test_008_restart_the_app_via_browser_refresh_button(self):
        """
        DESCRIPTION: Restart the app via browser Refresh button
        EXPECTED: App is refreshed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Football')

    def test_009_tap_back_button(self):
        """
        DESCRIPTION: Tap Back button
        EXPECTED: User is redirected to the Homepage
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')

    def test_010_go_to_the_sport_landing_page_via_direct_link(self):
        """
        DESCRIPTION: Go to the <Sport> landing page via direct link
        EXPECTED: <Sport> landing page is opened
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state(state_name='Tennis')

    def test_011_tap_back_button(self):
        """
        DESCRIPTION: Tap back button
        EXPECTED: User is redirected to the Homepage (user is not thrown out from the app)
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')

    def test_012_go_to_the_app_via_direct_link(self):
        """
        DESCRIPTION: Go to the app via direct link
        EXPECTED: Oxygen app is opened
        """
        self.device.navigate_to(url='www.python.org')
        self.navigate_to_page(name='home')
        self.site.wait_content_state(state_name='HomePage')

    def test_013_navigate_inside_the_app(self):
        """
        DESCRIPTION: Navigate inside the app
        EXPECTED: User is successfully navigated inside the app
        """
        self.site.open_sport(name=self.get_sport_title(self.ob_config.horseracing_config.category_id))

    def test_014_tap_back_button_several_times(self):
        """
        DESCRIPTION: Tap Back button several times
        EXPECTED: User is redirected to the Oxygen Homepage (user is not thrown out from the app)
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')

    def test_015_go_to_in_play_page_from_sports_menu_ribbon(self):
        """
        DESCRIPTION: Go to 'In-Play' page from Sports Menu Ribbon
        EXPECTED: 'In-Play' page is opened
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            sports.get('IN-PLAY').click()
        else:
            self.site.open_sport(name='IN-PLAY')

    def test_016_navigate_within_in_play_page_through_the_sport_race_tabs(self):
        """
        DESCRIPTION: Navigate within 'In-Play' page (through the Sport/Race tabs)
        EXPECTED: Sport/Race tab is opened on In-Play Landing page
        """
        try:
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        except (VoltronException, StaleElementReferenceException):
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        sport_name, sport = list(sports.items())[1]
        sport.click()  # BMA-49471
        try:
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        except (VoltronException, StaleElementReferenceException):
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports[sport_name].is_selected(timeout=10),
                        msg=f'"{sport_name}" is not selected after clicking on it')

        sport_item_name, _ = list(sports.items())[2]
        self.site.inplay.inplay_sport_menu.click_item(sport_item_name)
        try:
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        except (VoltronException, StaleElementReferenceException):
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports[sport_item_name].is_selected(), msg=f'{sport_item_name} is not selected after clicking on it')
        self.assertTrue(self.site.inplay.inplay_sport_menu.items_as_ordered_dict,
                        msg='There is not any sport in In-Play tab')

    def test_017_navigate_to_the_sport_race_event_details_page(self):
        """
        DESCRIPTION: Navigate to the Sport/Race Event Details page
        EXPECTED: Sport/Race Event Details page is opened
        """
        tab_content = self.site.inplay.tab_content
        sections = tab_content.accordions_list.items_as_ordered_dict
        if not sections:
            sections = tab_content.upcoming.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on page')
        section_name, section = list(sections.items())[0]
        self._logger.debug(f'*** Got section "{section_name}"')
        section.expand()
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events on "{section_name}"')
        event_name, event = list(events.items())[0]
        event.scroll_to_we()
        self._logger.debug(f'*** Got event "{event_name}"')
        event.click()
        self.assertTrue(any((self.site.wait_content_state('EventDetails', raise_exceptions=False, timeout=5),
                             self.site.wait_content_state('RacingEventDetails', raise_exceptions=False, timeout=5),
                             self.site.wait_content_state('GreyHoundEventDetails', raise_exceptions=False, timeout=5))),
                        msg='Event details page doesn\'t open')

    def test_018_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on Back button
        EXPECTED: Appropriate Sport/Race tab on In-Play Landing page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='InPlay')
        try:
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        except (VoltronException, StaleElementReferenceException):
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        sport_name, _ = list(sports.items())[2]
        sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports[sport_name].is_selected(), msg=f'"{sport_name}" is not selected')

    def test_019_tap_on_back_button_one_more_time(self):
        """
        DESCRIPTION: Tap on Back button one more time
        EXPECTED: * User is redirected to the 'In-Play' view
        EXPECTED: * The 'In-Play' icon the user navigated from is selected
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='InPlay')

    def test_020_go_to_a_z_page_from_sports_menu_ribbon_navigate_within_a_z_view_tap_back_button(self):
        """
        DESCRIPTION: Go to 'A-Z' page from Sports Menu Ribbon -> navigate within 'A-Z' view -> tap Back button
        EXPECTED: User is redirected to the 'A-Z' page from Sports Menu Ribbon he/she navigated from
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')
        self.site.open_sport(name='FOOTBALL')
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')
