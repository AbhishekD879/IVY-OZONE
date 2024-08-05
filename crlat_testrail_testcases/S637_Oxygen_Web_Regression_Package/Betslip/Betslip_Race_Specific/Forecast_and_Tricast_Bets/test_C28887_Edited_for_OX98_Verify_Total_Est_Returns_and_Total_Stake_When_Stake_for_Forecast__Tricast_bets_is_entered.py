import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C28887_Edited_for_OX98_Verify_Total_Est_Returns_and_Total_Stake_When_Stake_for_Forecast__Tricast_bets_is_entered(Common):
    """
    TR_ID: C28887
    NAME: [Edited for OX98] Verify 'Total Est. Returns' and 'Total Stake'  When Stake for Forecast / Tricast bets is entered
    DESCRIPTION: AUTOTEST: [C2552908]
    DESCRIPTION: This test case verifies the calculation of 'Total Est. Returns' and 'Total Stake' values when stake amount is entered for Forecast / Tricast bets.
    PRECONDITIONS: 1. Login with user
    PRECONDITIONS: 2. Navigate to Horse racing page
    PRECONDITIONS: 3. Open any rase event -> Navigate to Forecast/Tricast tab
    PRECONDITIONS: 4. Add Forecast/Tricast bets to Betslip
    PRECONDITIONS: **For earlier releases than OX98: For Forecast/Tricast bet - Add two or more selections from the same market to the Bet Slip**
    """
    keep_browser_open = True

    def test_001_open_betslipverify_that_est_returns_is_na_and_total_est_returns_is_000(self):
        """
        DESCRIPTION: Open 'BetSlip'
        DESCRIPTION: Verify that Est. Returns is N/A and Total Est. Returns is 0.00
        EXPECTED: Bet Slip is opened
        EXPECTED: Est. Returns is N/A
        EXPECTED: Total Est. Returns is 0.00
        """
        pass

    def test_002_enter_stake_amount_manually_in_a_stake_field_for_any_forecast_k_or_tricast_k_etc_bet_and_verify_total_est_returns_and_total_stake_fields(self):
        """
        DESCRIPTION: Enter stake amount manually in a 'Stake:' field for any 'Forecast (k)' or 'Tricast (k)' etc. bet and verify **'Total Est. Returns' and 'Total Stake'** fields
        EXPECTED: *   'Stake' field is pre-populated with entered value
        EXPECTED: *   **'Total Est. Returns'** is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: *   **'Total Stake'** = stake_amount*k,
        EXPECTED: where:
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: stake_amount - the stake which is entered manually
        """
        pass

    def test_003_log_out_and_log_in_with_user_who_has_free_bets_availableadd_forecasttricast_bets_to_betslip(self):
        """
        DESCRIPTION: Log out and log in with user who has free bets available
        DESCRIPTION: Add Forecast/Tricast bets to Betslip
        EXPECTED: User is logged in
        """
        pass

    def test_004_enter_stake_via_free_bets_and_verify_total_est_returns_and_total_stake_fields(self):
        """
        DESCRIPTION: Enter stake via free bets and verify **'Total Est. Returns'** and **'Total Stake'** fields
        EXPECTED: 'Stake' field is NOT pre-populated with a value selected in free bet drop-down
        EXPECTED: **'Total Est. Returns'** is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: **'Total Stake'** = free_bet,
        EXPECTED: where free_bet - free bet amount selected in the drop down
        """
        pass

    def test_005_enter_stake_via_free_bets_and_enter_stake_manually___verifytotal_est_returns_and_total_stake_fields(self):
        """
        DESCRIPTION: Enter stake via free bets AND enter stake manually -> verify **'Total Est. Returns'** and **'Total Stake'** fields
        EXPECTED: *   'Stake' field is pre-populated with entered value
        EXPECTED: *   **'Total Est. Returns'** is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: *   **'Total Stake'** = free_bet + stake_amount*k
        EXPECTED: where:
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: free_bet - free bet amount selected in the drop down
        EXPECTED: stake_amount - the stake which is entered manually
        """
        pass
