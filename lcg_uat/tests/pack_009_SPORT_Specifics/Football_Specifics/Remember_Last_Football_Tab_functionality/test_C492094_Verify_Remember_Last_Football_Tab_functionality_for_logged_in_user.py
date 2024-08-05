import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.football
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.safari
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.timeout(1020)
@pytest.mark.login
@vtest
class Test_C492094_Verify_Remember_Last_Football_Tab_functionality_for_logged_in_user(BaseSportTest):
    """
    TR_ID: C492094
    VOL_ID: C9697820
    NAME: Verify Remember Last Football Tab functionality for logged in user
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
        self.site.login()

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: Matches tab is selected by default and highlighted
        """
        self.site.open_sport(name=self.sport_name)
        self.assertEqual(self.site.football.tabs_menu.current,
                         self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                 self.ob_config.football_config.category_id),
                         msg='Matches tab is not active by default')

    def test_003_choose_in_play_tab(self, tab=None):
        """
        DESCRIPTION: Choose 'IN-PLAY' tab
        EXPECTED: 'IN-PLAY' tab is selected and highlighted
        EXPECTED: Appropriate events are displayed on In-Play page
        """
        if not tab:
            tab = self.__class__.in_play_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                                            self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(tab)
        self.verify_last_football_tab(tab=tab)

    def test_004_refresh_the_page(self, tab=None):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'IN-PLAY' tab is still selected and highlighted
        EXPECTED: Appropriate events are displayed on In-Play page
        """
        if not tab:
            tab = self.in_play_tab_name
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.verify_last_football_tab(tab=tab)

    def test_005_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage or other areas of application
        """
        self.site.back_button_click()

    def test_006_return_to_football_landing_page(self, tab=None):
        """
        DESCRIPTION: Return to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: In-Play tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for In-Play tab
        """
        if not tab:
            tab = self.in_play_tab_name
        self.site.open_sport(name=self.sport_name)
        self.verify_last_football_tab(tab=tab)

    def test_007_repeat_steps_3_6_for_other_tabs(self):
        """
        DESCRIPTION: Repeat steps 3-6 for the next tabs:
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
        tab_names = self.site.football.tabs_menu.items_as_ordered_dict
        self.assertTrue(tab_names, msg='No one tab found')
        for tab in list(tab_names.keys()):
            self._logger.info('*** Repeating steps for tab %s' % tab)
            if tab in (self.expected_sport_tabs.player_bets, self.in_play_tab_name):
                continue
            self.test_003_choose_in_play_tab(tab=tab)
            self.test_004_refresh_the_page(tab=tab)
            self.test_005_navigate_to_homepage()
            self.test_006_return_to_football_landing_page(tab=tab)
