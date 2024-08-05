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
class Test_C9745357_Verify_that_Partial_Cash_Out_button_is_not_shown_in_case_cash_out_value_less_than_010(Common):
    """
    TR_ID: C9745357
    NAME: Verify that 'Partial Cash Out' button is not shown in case cash out value less than 0.10
    DESCRIPTION: This test case verifies that partial cash out is unavailable for bets, where cash out value less than 0.10
    PRECONDITIONS: 1. Login and place SINGLE bet with cash out available
    PRECONDITIONS: 2. Navigate to My Bets page
    PRECONDITIONS: NOTE: Test case should be run on Cash Out and on Open Bets tab
    PRECONDITIONS: You can check the appropriate attribute in Web Developer Tool>Network tab>https://cashout-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/bet-details?token=94223d7220a6bd2a12b2217979bede17a3d7674a72a0dbe01727a22d8a940697  - "partialCashoutAvailable" should be 'N'
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: You can check the appropriate attribute in Dev Tools -> Network tab -> WS filter (cashout request) - in initial bets response "partialCashoutAvailable" should be 'N'
    """
    keep_browser_open = True

    def test_001_stay_on_my_betcash_outopen_bets_tapverify_that_partial_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Stay on My Bet>Cash Out/Open Bets tap
        DESCRIPTION: Verify that 'Partial Cash Out' button is shown
        EXPECTED: 'Partial Cash Out' button is shown
        """
        pass

    def test_002_make_a_partial_cashout_with_cash_out_value_to_have_less_than_or_equal_to_010_remainedverify_that_partial_cash_out_button_is_disappeared(self):
        """
        DESCRIPTION: Make a Partial cashout with cash out value to have less than or equal to 0.10 remained
        DESCRIPTION: Verify that 'Partial Cash Out' button is disappeared
        EXPECTED: 'Partial Cash Out' button is not shown
        EXPECTED: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
        EXPECTED: - 'Partial Cash Out' button is not shown
        EXPECTED: - Cashout MS will send cashoutUpdate with new 'cashoutValue'
        """
        pass

    def test_003_provide_the_same_verification_for_multiple_betverify_that_patrial_cash_out_button_is_not_shown_when_cash_out_value_less_than_010(self):
        """
        DESCRIPTION: Provide the same verification for MULTIPLE bet
        DESCRIPTION: Verify that 'Patrial Cash Out' button is not shown when cash out value less than 0.10
        EXPECTED: 'Patrial Cash Out' button is not shown
        """
        pass
