import pytest

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.football
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.slow
@pytest.mark.timeout(1200)
@vtest
class Test_C492238_Verify_Remember_Last_Football_Tab_functionality_for_logged_out_user(BaseSportTest):
    """
    TR_ID: C492238
    NAME: Verify Remember Last Football Tab functionality for logged out user
    """
    keep_browser_open = True
    sport_name = 'Football'

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: Matches tab is selected by default and highlighted
        """
        self.site.open_sport(name=self.sport_name)
        self.__class__.matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                  self.ob_config.football_config.category_id)
        self.assertEqual(self.site.football.tabs_menu.current, self.matches_tab_name,
                         msg=f'"{self.matches_tab_name}" tab is not active by default')

    def test_002_choose_in_play_tab(self, tab=None):
        """
        DESCRIPTION: Choose 'IN-PLAY' tab
        EXPECTED: 'IN-PLAY' tab is selected and highlighted
        EXPECTED: Appropriate events are displayed on In-Play page
        """
        if not tab:
            tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(tab)
        self.verify_last_football_tab(tab=tab)

    def test_003_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        """
        self.site.back_button_click()
        self.site.wait_content_state('Homepage')

    def test_004_return_to_football_landing_page(self):
        """
        DESCRIPTION: Return to Football Landing page
        EXPECTED: Football Landing page is opened
        EXPECTED: Matches tab is selected and highlighted
        EXPECTED: Appropriate content is displayed for Matches tab
        """
        self.site.open_sport(name=self.sport_name)
        self.verify_last_football_tab(tab=self.matches_tab_name)

    def test_005_repeat_steps_2_4_for_other_tabs(self):
        """
        DESCRIPTION: Repeat steps 2-4 for the next tabs:
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
        for tab in tabs.keys():
            self._logger.info(f'*** Repeating steps for tab "{tab}"')
            if tab in (self.expected_sport_tabs.player_bets, self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                                                     self.ob_config.football_config.category_id)):
                continue
            self.test_002_choose_in_play_tab(tab=tab)
            self.test_003_navigate_to_homepage()
            self.test_004_return_to_football_landing_page()
