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
class Test_C9752213_Verify_that_Partial_Cash_Out_button_is_not_shown_in_case_bet_is_placed_with_free_bet(Common):
    """
    TR_ID: C9752213
    NAME: Verify that 'Partial Cash Out' button is not shown in case bet is placed with free bet
    DESCRIPTION: This test case verifies that partial cash out is unavailable for bets which were placed with Free Bet Offer
    PRECONDITIONS: 1. Login and place bet with cash out available using Free Bet Offer
    PRECONDITIONS: 2. Navigate to My Bets page
    PRECONDITIONS: NOTE: Test case should be run on Cash Out and on Open Bets tab
    PRECONDITIONS: You can check the appropriate attribute in Web Developer Tool>Network tab>https://cashout-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/bet-details?token=94223d7220a6bd2a12b2217979bede17a3d7674a72a0dbe01727a22d8a940697  - "partialCashoutAvailable" should be 'N'
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    PRECONDITIONS: You can check the appropriate attribute in Dev Tools -> Network tab -> WS filter (cashout request) - in initial bets response "partialCashoutAvailable" should be 'N'
    """
    keep_browser_open = True

    def test_001_verify_that_patrial_cash_out_button_is_not_shown_for_the_bet_on_cash_out_and_on_open_bets_tabs(self):
        """
        DESCRIPTION: Verify that 'Patrial Cash Out' button is not shown for the bet on Cash Out and on Open bets tabs
        EXPECTED: Patrial Cash Out' button is not shown
        """
        pass

    def test_002_provide_the_same_verification_for_multiple_betverify_that_patrial_cash_out_button_is_not_shown_multiple_bet_placed_with_free_bet_offer(self):
        """
        DESCRIPTION: Provide the same verification for MULTIPLE bet
        DESCRIPTION: Verify that 'Patrial Cash Out' button is not shown multiple bet placed with Free Bet Offer
        EXPECTED: 'Patrial Cash Out' button is not shown
        """
        pass
