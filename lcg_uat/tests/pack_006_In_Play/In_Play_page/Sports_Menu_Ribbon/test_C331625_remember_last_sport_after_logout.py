import pytest
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.login
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-46013')  # Coral Desktop only
class Test_C331625_Verify_remember_last_Sport_functionality_on_In_Play_page_after_Logout(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C331625
    NAME: Verify remember last Sport functionality on In-Play page after Logout
    DESCRIPTION: This test case verifies remember last Sport functionality on In-Play page after Logout
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: **TI (events) config:**
    PRECONDITIONS: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Category, where X.XX - the latest OpenBet release
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Log in
    """
    keep_browser_open = True
    sport_name = 'In-Play'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        PRECONDITIONS: Log in
        """
        self.__class__.username = tests.settings.betplacement_user
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self.__class__.team1 = list(self.selection_ids.keys())[0]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
                event_params.team1, event_params.team2, event_params.selection_ids
        self._logger.info(f'*** Found Football event with selection ids "{self.selection_ids}"')
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_001_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            inplay = sports.get('IN-PLAY', None)
            self.assertTrue(inplay, msg='Can not get "IN-PLAY" sport tab')
            inplay.click()
            self.assertTrue(sports['IN-PLAY'].is_selected(), msg='IN-PLAY is not selected after clicking on it')
        else:
            self.site.open_sport(name=self.sport_name, timeout=10)
        try:
            self.assertTrue(self.site.inplay.inplay_sport_menu.items_as_ordered_dict,
                            msg='There is not any sport in In-Play tab')
        except (VoltronException, StaleElementReferenceException):
            self.assertTrue(self.site.inplay.inplay_sport_menu.items_as_ordered_dict,
                            msg='There is not any sport in In-Play tab')
        self.__class__.chosen_sport = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.keys())[2]
        self.__class__.default_sport = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.keys())[1]
        self.verify_active_sport_on_inplay_page(self.default_sport)

    def test_002_choose_any_sports_icon(self):
        """
        DESCRIPTION: Choose any Sports icon
        EXPECTED: * Selected Sports tab is underlined by red line
        EXPECTED: * The appropriate content is displayed for selected Sports
        """
        self.site.inplay.inplay_sport_menu.click_item(self.chosen_sport)
        self.verify_active_sport_on_inplay_page(self.chosen_sport)

    def test_003_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is logged out successfully
        """
        self.site.logout()

    def test_004_navigate_to_in_play_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            inplay = sports.get('IN-PLAY', None)
            self.assertTrue(inplay, msg='Can not get "IN-PLAY" sport tab')
            inplay.click()
            self.assertTrue(sports['IN-PLAY'].is_selected(), msg='IN-PLAY is not selected after clicking on it')
        else:
            self.site.open_sport(name=self.sport_name, timeout=10)
        self.verify_active_sport_on_inplay_page(self.default_sport)

    def test_005_go_out_from_in_play_page(self):
        """
        DESCRIPTION: Go out from 'In-Play' page
        """
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='Homepage')

    def test_006_log_in_again_with_the_same_user_account(self):
        """
        DESCRIPTION: Log in again with the same user account
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_007_navigate_to_in_play_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * Tab from step 2 is selected and underlined by red line
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', sports.keys(), msg='IN-PLAY is not found in the header sport menu')
            inplay = sports.get('IN-PLAY', None)
            self.assertTrue(inplay, msg='Can not get "IN-PLAY" sport tab')
            inplay.click()
            self.assertTrue(sports['IN-PLAY'].is_selected(), msg='IN-PLAY is not selected after clicking on it')
        else:
            self.site.open_sport(name=self.sport_name, timeout=10)
        self.verify_active_sport_on_inplay_page(self.chosen_sport)

    def test_008_log_into_application_using_another_account(self):
        """
        DESCRIPTION: Log into application using another account
        EXPECTED: User is logged in successfully
        """
        self.test_003_log_out_from_application()
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_009_navigate_to_in_play_page(self):
        """
        DESCRIPTION: Navigate to 'In-Play' page
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        self.test_001_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header()

    def test_010_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is logged out successfully
        """
        self.test_003_log_out_from_application()

    def test_011_log_into_application_again_but_trigger_situation_when_there_are_no_in_play_events_for_saved_sport(self):
        """
        DESCRIPTION: Log into application again but trigger situation when there are no In-Play events for saved sport
        EXPECTED: * 'In-Play' page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        """
        # We should skip this step because it requires to delete all live events from some sport
