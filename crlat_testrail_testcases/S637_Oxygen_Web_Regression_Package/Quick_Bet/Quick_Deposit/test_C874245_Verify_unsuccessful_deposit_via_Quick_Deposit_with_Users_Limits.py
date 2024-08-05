import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C874245_Verify_unsuccessful_deposit_via_Quick_Deposit_with_Users_Limits(Common):
    """
    TR_ID: C874245
    NAME: Verify unsuccessful deposit via Quick Deposit with User`s Limits
    DESCRIPTION: This test case verifies unsuccessful deposit via Quick Deposit with User`s Limits
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in and has set Deposit Limits
    PRECONDITIONS: 4. Users have the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance_and_is_greater_than_deposit_limits_dailyweeklymonthly(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance and is greater than Deposit limits (daily/weekly/monthly)
        EXPECTED: * Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for **Ladbrokes** brand
        EXPECTED: * The same message(without icon) is displayed below 'QUICK BET' header for **Coral** brand
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered stake value and users balance
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * 'QUICK DEPOSIT' section is displayed within Quick Bet
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        """
        pass

    def test_005_select_visa_card(self):
        """
        DESCRIPTION: Select **Visa** card
        EXPECTED: **Visa** card is selected
        """
        pass

    def test_006_enter_valid_cvv_in_cvv_field(self):
        """
        DESCRIPTION: Enter valid CVV in 'CVV' field
        EXPECTED: * 'Deposit Amount' and 'CVV' fields are populated with values
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes enabled
        """
        pass

    def test_007_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: * **This deposit would exceed your self-imposed deposit limit. Check your current limit here.** warning message is shown on yellow/cyan background below 'QUICK DEPOSIT' header
        EXPECTED: ,where 'here' is the hyperlink
        EXPECTED: * Quick Deposit remains opened
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        EXPECTED: * CVV field is cleared
        """
        pass

    def test_008_tap_here_hyperlink_for_coral(self):
        """
        DESCRIPTION: Tap 'here' hyperlink (for Coral)
        EXPECTED: * User is navigated to 'Limits' page
        EXPECTED: * Quick Bet is closed
        """
        pass

    def test_009_repeat_steps_2_7_with_a_stake_value_that_will_force_you_to_deposit_your_daily_limit_sum(self):
        """
        DESCRIPTION: Repeat steps 2-7 with a stake value that will force you to deposit your 'Daily' limit sum
        EXPECTED: Bet is placed successfully
        EXPECTED: Placed bet value is deducted from user's Balance
        """
        pass

    def test_010_repeat_steps_2_7_with_a_same_condition_that_a_stake_value_will_force_you_to_deposit_your_daily_limit_sum(self):
        """
        DESCRIPTION: Repeat steps 2-7 with a same condition that a stake value will force you to deposit your 'Daily' limit sum
        EXPECTED: * **We are sorry, but your daily limit has been exceeded. You can review your deposits limits on the Responsible Gaming page in Casino My Account.** warning message is shown on yellow/cyan background below 'QUICK DEPOSIT' header
        EXPECTED: * Quick Deposit remains opened
        EXPECTED: * User Balance is not changed
        EXPECTED: * Entered amount is not cleared
        EXPECTED: * CVV field is cleared
        """
        pass

    def test_011_select_visa_electron_card_and_repeat_steps_2_8_and_910(self):
        """
        DESCRIPTION: Select **Visa Electron** card and repeat steps #2-8 and 9,10
        EXPECTED: 
        """
        pass

    def test_012_select_master_card_card_and_repeat_steps_2_8_and_910(self):
        """
        DESCRIPTION: Select **Master Card** card and repeat steps #2-8 and 9,10
        EXPECTED: 
        """
        pass

    def test_013_select_maestro_card_and_repeat_steps_2_8_and_910(self):
        """
        DESCRIPTION: Select **Maestro** card and repeat steps #2-8 and 9,10
        EXPECTED: 
        """
        pass
