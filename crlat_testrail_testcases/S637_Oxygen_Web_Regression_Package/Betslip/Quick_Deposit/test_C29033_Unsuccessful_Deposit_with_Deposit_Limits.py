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
class Test_C29033_Unsuccessful_Deposit_with_Deposit_Limits(Common):
    """
    TR_ID: C29033
    NAME: Unsuccessful Deposit with Deposit Limits
    DESCRIPTION: This test case verifies Unsuccessful Depositing functionality on the Bet Slip page via credit/debit cards and cancellation because of Set Deposit Limits.
    DESCRIPTION: AUTOTEST [C2352430]
    PRECONDITIONS: * Load app and log in with a user that has at list one credit card added
    PRECONDITIONS: * Add selection to Betslip
    """
    keep_browser_open = True

    def test_001_enter_stake_amount_greater_than_deposit_limitsdailyweeklymonthly_and_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount greater than Deposit limits(daily/weekly/monthly) and that exceeds user`s balance
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_002_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'Deposit Amount' field is pre-populated with entered value in case when needed amount >or= 5/50 for SEK
        EXPECTED: * 'Deposit Amount' field is empty in case when needed amount < 5/50 for SEK
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET'
        """
        pass

    def test_003_enter_valid_cvv_into_cvv_field_and_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Enter valid CVV into 'CVV' field and Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: *   [Coral] Error message appears within 'Quick Deposit' content area inside the 'i' information message :
        EXPECTED: **"This deposit would exceed your self-imposed deposit limit. Check your current limit here(<link>)."**
        EXPECTED: *   User remains on the 'Bet Slip'
        EXPECTED: *   User Balance is not changed
        EXPECTED: *   Entered amount is not cleared
        EXPECTED: *   CVV field is cleared
        """
        pass

    def test_004_click_here_link(self):
        """
        DESCRIPTION: Click **here** link
        EXPECTED: User is navigated to **My Limits** page
        """
        pass

    def test_005_repeat_steps_1_3_with_a_stake_value_that_will_force_you_to_deposit_your_daily_limit_sum(self):
        """
        DESCRIPTION: Repeat steps 1-3 with a stake value that will force you to deposit your 'Daily' limit sum
        EXPECTED: Bet is placed successfully
        EXPECTED: Placed bet value is deducted from user's Balance
        """
        pass

    def test_006_repeat_steps_1_3_with_a_same_condition_that_a_stake_value_will_force_you_to_deposit_your_daily_limit_sum(self):
        """
        DESCRIPTION: Repeat steps 1-3 with a same condition that a stake value will force you to deposit your 'Daily' limit sum
        EXPECTED: *   [Coral]Error message appears within 'Quick Deposit' content area inside the 'i' information message :
        EXPECTED: * 'We are sorry, but your daily limit has been exceeded. You can review your deposits limits on the Responsible Gaming page in Casino My Account.'
        EXPECTED: Quick Deposit remains opened
        EXPECTED: User Balance is not changed
        EXPECTED: Entered amount is not cleared
        EXPECTED: CVV field is cleared
        """
        pass
