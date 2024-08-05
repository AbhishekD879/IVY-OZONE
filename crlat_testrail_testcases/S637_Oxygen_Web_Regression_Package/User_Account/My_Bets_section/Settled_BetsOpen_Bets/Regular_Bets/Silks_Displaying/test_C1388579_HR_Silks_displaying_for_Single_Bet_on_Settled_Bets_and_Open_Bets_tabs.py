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
class Test_C1388579_HR_Silks_displaying_for_Single_Bet_on_Settled_Bets_and_Open_Bets_tabs(Common):
    """
    TR_ID: C1388579
    NAME: HR Silks displaying for Single Bet on Settled Bets and Open Bets tabs
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled Bets
    DESCRIPTION: AUTOTEST [C2600785]
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Single bet on Horse Racing races with silks
    PRECONDITIONS: User has placed Single bet on Horse Racing races with silks and the bet is already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_silk_is_displaying_for_single_horse_racing_bet(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for Single horse racing bet
        EXPECTED: - Correct silk is displayed for placed bet to the left of a horse name
        """
        pass

    def test_002_navigate_to_settled_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_silk_is_displaying_for_single_horse_racing_settled_bet(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that Silk is displaying for Single horse racing settled bet
        EXPECTED: - Correct silk is displayed for settled bet to the left of a horse name
        """
        pass
