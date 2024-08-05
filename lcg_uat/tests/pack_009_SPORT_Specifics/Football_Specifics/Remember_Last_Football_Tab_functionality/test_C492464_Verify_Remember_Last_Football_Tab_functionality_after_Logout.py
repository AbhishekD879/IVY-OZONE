import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.football
@pytest.mark.sports
@pytest.mark.low
@pytest.mark.slow
@pytest.mark.timeout(1200)
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C492464_Verify_Remember_Last_Football_Tab_functionality_after_Logout(BaseSportTest):
    """
    TR_ID: C492464
    NAME: Verify Remember Last Football Tab functionality after Logout
    DESCRIPTION: This test case verifies Remember Last Football Tab functionality after Logout
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True
    sport_name = 'Football'

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        EXPECTED: Homepage is loaded
        EXPECTED: User is logged in
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username, async_close_dialogs=False, timeout_close_dialogs=5)

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: Matches tab is selected by default and highlighted
        """
        self.__class__.football_id = self.ob_config.football_config.category_id
        self.site.open_sport(name=self.sport_name)
        self.__class__.matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                  self.football_id)
        self.assertEqual(self.site.football.tabs_menu.current, self.matches_tab_name,
                         msg=f'"{self.matches_tab_name}" tab is not active by default')

    def test_003_choose_in_play_tab(self, tab=None):
        """
        DESCRIPTION: Choose 'IN-PLAY' tab
        EXPECTED: 'IN-PLAY' tab is selected and highlighted
        EXPECTED: Appropriate events are displayed on In-Play page
        """
        if not tab:
            self.__class__.in_play_presence = self.is_tab_present(
                tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, category_id=self.football_id) or \
                (self.device_type == 'desktop')

            in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                  self.ob_config.football_config.category_id)

            if self.device_type == 'desktop':
                self.__class__.in_play_tab_name = in_play_tab  # IN-PLAY tab is hardcoded to desktop
                self.assertTrue(self.site.football.tabs_menu.click_button(self.in_play_tab_name),
                                msg=f'"{self.in_play_tab_name}" is not opened')
                self.verify_last_football_tab(tab=self.in_play_tab_name)
            elif self.in_play_presence:
                self.__class__.in_play_tab_name = in_play_tab
                self.site.football.tabs_menu.click_button(self.in_play_tab_name)
                self.verify_last_football_tab(tab=self.in_play_tab_name)
            else:
                self._logger.warning(f'*** "{in_play_tab}" tab is not supposed to be present. '
                                     f'Probably it is disabled in CMS. Skipping verification of presence.')
        else:
            self.site.football.tabs_menu.click_button(tab)
            self.verify_last_football_tab(tab=tab)

    def test_004_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is successfully logged out
        """
        self.site.logout()

    def test_005_return_to_football_landing_page(self, tab=None):
        """
        DESCRIPTION: Log into app and return to Football Landing page
        EXPECTED: User is successfully logged in
        EXPECTED: Football Landing page is opened
        EXPECTED: In-Play tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for In-Play tab
        """
        self.site.login(username=self.username, async_close_dialogs=False, timeout_wait_for_dialog=2, timeout_close_dialogs=5)
        self.site.open_sport(name=self.sport_name)
        if not tab:
            if self.in_play_presence:
                self.verify_last_football_tab(tab=self.in_play_tab_name)
            else:
                self._logger.warning(f'*** "{self.in_play_tab}" tab is not supposed to be present. '
                                     f'Probably it is disabled in CMS. Skipping verification.')
        else:
            self.verify_last_football_tab(tab=tab)

    def test_006_repeat_steps_3_5_for_other_tabs(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the next tabs:
        DESCRIPTION: * Matches
        DESCRIPTION: * Competitions
        DESCRIPTION: * Coupons
        DESCRIPTION: * Outrights
        DESCRIPTION: * Specials
        DESCRIPTION: * Jackpot
        EXPECTED: Football Landing page is opened
        EXPECTED: Previously chosen tab is displayed as selected and highlighted
        EXPECTED: Appropriate content is displayed for selected tab
        """
        tabs = self.site.football.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='Tabs are empty')
        if self.in_play_presence:
            del tabs[self.in_play_tab_name]
        for tab in tabs.keys():
            self._logger.info(f'*** Repeating steps for tab {tab}')
            if tab == self.expected_sport_tabs.player_bets:
                continue
            self.test_003_choose_in_play_tab(tab=tab)
            self.test_004_log_out_from_app()
            self.test_005_return_to_football_landing_page(tab=tab)
