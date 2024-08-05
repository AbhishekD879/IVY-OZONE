import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.low
@pytest.mark.football
@pytest.mark.sports
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.slow
@pytest.mark.timeout(1020)
@vtest
class Test_C492472_Verify_Remember_Last_Football_Tab_functionality_after_Login_with_Different_User(BaseSportTest):
    """
    TR_ID: C492472
    VOL_ID: C9697803
    NAME: Verify Remember Last Football Tab functionality after Login with Different User
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
        self.__class__.username2 = tests.settings.betplacement_user
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: Matches tab is selected by default and highlighted
        """
        self.site.open_sport(name=self.sport_name)
        self.__class__.matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                  self.ob_config.football_config.category_id)
        self.assertEqual(self.site.football.tabs_menu.current, self.matches_tab_name,
                         msg='"%s" tab is not active by default' % self.matches_tab_name)

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

    def test_004_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is successfully logged out
        """
        self.site.logout()

    def test_005_log_into_app_with_another_user_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app with ANOTHER user and return to Football Landing page
        EXPECTED: User is successfully logged in
        EXPECTED: Football Landing page is opened
        EXPECTED: 'MATCHES' tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for 'MATCHES' tab
        """
        self.site.login(username=self.username2, async_close_dialogs=False)
        self.site.open_sport(name=self.sport_name)
        self.verify_last_football_tab(tab=self.matches_tab_name)

    def test_006_choose_any_tab_except_in_play_and_matches(self):
        """
        DESCRIPTION: Choose any tab except 'IN-PLAY' and 'MATCHES'
        EXPECTED: Tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for selected tab
        """
        self.__class__.competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                                       self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(self.competitions_tab_name)
        self.verify_last_football_tab(tab=self.competitions_tab_name)

    def test_007_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is successfully logged out
        """
        self.site.logout()

    def test_008_log_into_app_with_first_user_from_step_1_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app with user from step 1 and return to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: 'IN-PLAY' tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for 'IN-PLAY' tab
        """
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.open_sport(name=self.sport_name)
        self.verify_last_football_tab(tab=self.in_play_tab_name)

    def test_009_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is successfully logged out
        """
        self.site.logout()

    def test_010_log_into_app_with_user_from_step_5_and_return_to_football_landing_page(self):
        """
        DESCRIPTION: Log into app with user from step 5 and return to Football Landing page
        EXPECTED: User is successfully logged in
        EXPECTED: Football Landing page is opened
        EXPECTED: Tab from step 6 is selected and highlighted
        EXPECTED: Appropriate content is displayed for selected tab
        """
        self.site.login(username=self.username2, async_close_dialogs=False)
        self.site.open_sport(name=self.sport_name)
        self.verify_last_football_tab(tab=self.competitions_tab_name)
