import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C23820437_To_edit_Vanilla_Verify_unsuccessful_deposit_via_Quick_Deposit_with_Users_Limits(Common):
    """
    TR_ID: C23820437
    NAME: [To edit] [Vanilla] Verify unsuccessful deposit via Quick Deposit with User's Limits
    DESCRIPTION: This test case verifies unsuccessful deposit via Quick Deposit with User's Limits
    DESCRIPTION: **Autotest**
    DESCRIPTION: C48912020
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user's settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in and has set Deposit Limits
    PRECONDITIONS: 4. Users have Creditcard added to his account
    PRECONDITIONS: 5. App is loaded
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        pass

    def test_002_enter_value_in_stake_field_that_exceeds_users_balance_and_is_greater_than_deposit_limits_dailyweeklymonthly(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance and is greater than Deposit limits (daily/weekly/monthly)
        EXPECTED: 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below 'QUICK BET' header
        """
        pass

    def test_003_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: Quick Deposit iFrame is displayed
        EXPECTED: 'MAKE A DEPOSIT' changed to 'DEPOSIT AND PLACE BET' button disabled by default
        """
        pass

    def test_004_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: 'Deposit Amount' and 'CVV' fields are populated with values
        EXPECTED: 'DEPOSIT & PLACE BET' button becomes enabled
        """
        pass

    def test_005_tap_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT AND PLACE BET' button
        EXPECTED: Warning message that self-set deposit limit exceeded is displayed
        EXPECTED: - Quick Deposit remains opened
        EXPECTED: - User Balance is not changed
        EXPECTED: - Entered amount is not cleared
        EXPECTED: - CVV field is cleared
        """
        pass

    def test_006_place_bet_with_a_stake_value_that_will_force_you_to_deposit_your_daily_limit_sum(self):
        """
        DESCRIPTION: Place Bet with a stake value that will force you to deposit your 'Daily' limit sum
        EXPECTED: Bet is placed successfully
        EXPECTED: Placed bet value is deducted from user's Balance if user's balance was positive
        """
        pass
