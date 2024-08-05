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
class Test_C2552920_HR_Silks_displaying_for_Forecast_Tricast_Bet_on_Settled_and_Open_Bets_tabs(Common):
    """
    TR_ID: C2552920
    NAME: HR Silks displaying for Forecast/Tricast Bet on Settled and Open Bets tabs
    DESCRIPTION: This test case verifies that HR Silks are displayed on Horse Racing bets on Open bets and Settled bets
    DESCRIPTION: AUTOTEST [C2600897]
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has placed Forecast/Tricast  bet on Horse Racing races with silks
    PRECONDITIONS: User has placed Forecast/Tricast  bet on Horse Racing races with silks and bet is already settled
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_correct_silk_is_displaying_for_placed_forecasttricast_horse_racing_bet(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that correct Silk is displaying for placed Forecast/Tricast horse racing bet
        EXPECTED: * Correct silks are displayed for placed bet
        EXPECTED: * Silks are displayed on the left of each horse name
        EXPECTED: * Silks with selection names are displayed one by one in column view
        """
        pass

    def test_002_navigate_to_settled_bets_tab_on_my_bets_pagebet_slip_widgetverify_that_correct_silk_is_displaying_for_settled_forecasttricast_horse_racing_bet(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify that correct Silk is displaying for settled Forecast/Tricast horse racing bet
        EXPECTED: * Correct silks are displayed for settled bet
        EXPECTED: * Silks are displayed on the left of each horse name
        EXPECTED: * Silks with selection names are displayed one by one in column view
        """
        pass
