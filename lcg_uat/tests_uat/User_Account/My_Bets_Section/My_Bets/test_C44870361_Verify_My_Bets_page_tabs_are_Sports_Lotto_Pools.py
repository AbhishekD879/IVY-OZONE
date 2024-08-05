import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870361_Verify_My_Bets_page_tabs_are_Sports_Lotto_Pools(Common):
    """
    TR_ID: C44870361
    NAME: Verify My Bets page tabs are 'Sports', 'Lotto', 'Pools'
    PRECONDITIONS: Uses is logged in
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: user must login
        """
        self.site.login()

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default.
        """
        if self.device_type == "mobile":
            self.site.wait_content_state("Homepage")
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            if self.brand == 'ladbrokes':
                featured_section = tabs.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME)
            else:
                featured_section = tabs.get(vec.racing.RACING_DEFAULT_TAB_NAME)
        else:
            tabs = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(tabs, msg=f'No "{tabs}" found on Home Page')
            if self.brand == 'ladbrokes':
                featured_section = tabs.get(vec.racing.RACING_FEATURED_TAB_NAME)
            else:
                featured_section = tabs.get(vec.racing.RACING_DEFAULT_TAB_NAME)
        self.assertTrue(featured_section.is_selected, msg=f'"{featured_section}" section not found')

    def test_002_click_on_my_betsorclick_on_my_bets_icon_on_footer_menuorclick_on_my_bets_in_bet_slip_for_desktoporclick_bet_history_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Click on My Bets
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets icon on Footer Menu.
        DESCRIPTION: or
        DESCRIPTION: Click on My Bets in Bet Slip (for Desktop)
        DESCRIPTION: or
        DESCRIPTION: Click Bet History via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: My Bets page should open.
        """
        self.site.open_my_bets_open_bets()

    def test_003_verify_sports_lotto_and_pools_tab_in_open_bets(self):
        """
        DESCRIPTION: Verify 'Sports', 'Lotto' and 'Pools' tab in 'Open Bets'
        EXPECTED: Customer should see all these three tabs
        EXPECTED: Sports Lotto Pools
        """
        if self.device_type == "mobile":
            actual_contents = list(self.site.open_bets.grouping_buttons.items_as_ordered_dict.keys())
        else:
            actual_contents = list(self.site.open_bets.tab_content.grouping_buttons.items_as_ordered_dict.keys())
        self.assertEqual(actual_contents, vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS,
                         msg=f'Tab "{actual_contents}" is not found in "{vec.bet_history.SORTING_BUTTON_TYPES_SETTLED_BETS}"')
