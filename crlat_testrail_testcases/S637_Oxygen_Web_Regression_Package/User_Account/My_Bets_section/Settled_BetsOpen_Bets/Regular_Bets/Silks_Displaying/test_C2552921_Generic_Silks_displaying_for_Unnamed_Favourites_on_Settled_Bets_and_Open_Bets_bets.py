import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2552921_Generic_Silks_displaying_for_Unnamed_Favourites_on_Settled_Bets_and_Open_Bets_bets(Common):
    """
    TR_ID: C2552921
    NAME: Generic Silks displaying for Unnamed Favourites on Settled Bets and Open Bets bets
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Bet History
    DESCRIPTION: AUTOTEST [C2554280]
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed a bet on Unnamed Favourite and Unnamed 2nd Favourite
    PRECONDITIONS: User has placed a bet on Unnamed Favourite and Unnamed 2nd Favourite and the bet is already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widgetverify_single_horse_racing_bet_placed_on_unnamed_favourite(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify Single horse racing bet placed on Unnamed Favourite
        EXPECTED: Generic grey silk image is displayed for placed bet
        """
        pass

    def test_002_verify_single_horse_racing_bet_placed_on_unnamed_2nd_favourite(self):
        """
        DESCRIPTION: Verify Single horse racing bet placed on Unnamed 2nd Favourite
        EXPECTED: Generic grey silk image is displayed for placed bet
        """
        pass

    def test_003_navigate_to_settled_bets_tab_on_my_bets_pagebet_slip_widgetverify_single_horse_racing_bet_placed_on_unnamed_favourite(self):
        """
        DESCRIPTION: Navigate to 'Settled bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify Single horse racing bet placed on Unnamed Favourite
        EXPECTED: Generic grey silk image is displayed for settled bet
        """
        pass

    def test_004_verify_single_horse_racing_bet_placed_on_unnamed_2nd_favourite(self):
        """
        DESCRIPTION: Verify Single horse racing bet placed on Unnamed 2nd Favourite
        EXPECTED: Generic grey silk image is displayed for settled bet
        """
        pass
