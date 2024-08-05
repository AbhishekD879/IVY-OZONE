import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2552919_HR_Silks_displaying_for_Multiple_Bet_on_Settled_Bets_and_Open_Bets_tabs(Common):
    """
    TR_ID: C2552919
    NAME: HR Silks displaying for Multiple Bet on Settled Bets and Open Bets tabs
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Bet History
    DESCRIPTION: AUTOTEST [C2600997]
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Multiple bet on Horse Racing races with silks
    PRECONDITIONS: User has placed Multiple bet on Horse Racing races with silks and the bet is already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_silk_is_displaying_for_placed_multiple_horse_racing_bet(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for placed Multiple horse racing bet
        EXPECTED: * Correct silks are displayed for placed bet
        EXPECTED: * Silks are displayed on the left of each horse name
        """
        pass

    def test_002_navigate_to_settled_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_silk_is_displaying_for_settled_multiple_horse_racing_bet(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for settled Multiple horse racing bet
        EXPECTED: * Correct silks are displayed for settled bet
        EXPECTED: * Silks are displayed on the left of each horse name
        """
        pass
