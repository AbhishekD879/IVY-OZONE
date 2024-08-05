import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870361_Verify_My_Bets_page_tabs_are_Sports_Lotto_Pools(Common):
    """
    TR_ID: C44870361
    NAME: Verify My Bets page tabs are 'Sports', 'Lotto', 'Pools'
    DESCRIPTION: 
    PRECONDITIONS: Uses is logged in
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default.
        """
        pass

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
        pass

    def test_003_verify_sports_lotto_and_pools_tab_in_open_bets(self):
        """
        DESCRIPTION: Verify 'Sports', 'Lotto' and 'Pools' tab in 'Open Bets'
        EXPECTED: Customer should see all these three tabs
        EXPECTED: Sports Lotto Pools
        """
        pass
