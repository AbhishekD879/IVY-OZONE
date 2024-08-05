import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2552924_No_Silks_selections_displaying_on_Settled_Bets_and_Open_Bets_tabs(Common):
    """
    TR_ID: C2552924
    NAME: No Silks selections displaying on Settled Bets and Open Bets tabs
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled Bets tabs
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed bets on **Horse Racing** races without silks (Singles, Multiple, Forecast/Tricast  bets);
    PRECONDITIONS: User has placed bets on **Horse Racing** races without silks (Singles, Multiple, Forecast/Tricast  bets) and the bets are already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widgetverify_single_horse_racing_bet_available_without_silks(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify Single horse racing bet available (without silks)
        EXPECTED: No silks are displayed to the left of a horse name
        """
        pass

    def test_002_verify_tricastforecast_horse_racing_bet_available_without_silks(self):
        """
        DESCRIPTION: Verify Tricast/Forecast horse racing bet available (without silks)
        EXPECTED: No silks are displayed to the left of a horse name
        """
        pass

    def test_003_verify_multiple_horse_racing_bet_available_without_silks(self):
        """
        DESCRIPTION: Verify Multiple horse racing bet available (without silks)
        EXPECTED: No silks are displayed to the left of a horse name
        """
        pass

    def test_004_navigate_to_settled_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_no_silks_also_not_displaying_for_settled_bets(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that No silks also not displaying for Settled bets
        EXPECTED: No silks are displayed to the left of a horse name for settled Single horse racing, Tricast/Forecast horse racing and Multiple horse racing bets
        """
        pass
