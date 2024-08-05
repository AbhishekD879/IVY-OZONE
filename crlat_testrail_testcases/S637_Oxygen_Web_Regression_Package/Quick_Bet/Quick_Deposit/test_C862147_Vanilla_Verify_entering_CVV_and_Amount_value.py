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
class Test_C862147_Vanilla_Verify_entering_CVV_and_Amount_value(Common):
    """
    TR_ID: C862147
    NAME: [Vanilla] Verify entering 'CVV' and 'Amount' value
    DESCRIPTION: This test case verifies entering stake value in a  'CVV' and 'Amount'  fields using numeric keyboard for Quick Deposit within Quick Bet
    DESCRIPTION: NOTE: **Vanilla** specific test case [C23820446]
    PRECONDITIONS: 1. Oxygen application is loaded
    PRECONDITIONS: 2. Log in under user account with  zero balance/positive balance and supported card types added
    PRECONDITIONS: (NOTE: if user has zero balance and added supported cards then quick deposit section is opened just after stake is entered in Quick Bet)
    """
    keep_browser_open = True

    def test_001_select_one_sportraces_selection(self):
        """
        DESCRIPTION: Select one <Sport>/<Races> selection
        EXPECTED: * Quick Bet is opened
        EXPECTED: * Added selection is displayed
        EXPECTED: * Numeric keyboard is collapsed by default
        """
        pass

    def test_002_enter_higher_than_user_balance_stake__and_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Enter higher than user balance stake  and tap on 'Make a Deposit' button
        EXPECTED: * Quick Deposit section appears
        EXPECTED: * Numeric keyboard is not shown
        EXPECTED: * 'CVV' field is empty by default
        EXPECTED: * 'Deposit Amount' field is pre-populated with amount with the difference from the balance and stake
        EXPECTED: * '-' and '+' buttons are displayed on both sides of deposit amount input field
        EXPECTED: * 'Quick Stakes' buttons are displayed below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_003_focus_cvv_field(self):
        """
        DESCRIPTION: Focus 'CVV' field
        EXPECTED: * 'CVV' field is focused
        EXPECTED: * 'Quick Stakes' buttons are NOT shown
        EXPECTED: * Numeric keyboard is opened with '.' button disabled
        EXPECTED: * 'DEPOSIT & PLACE BET' button is disabled
        """
        pass

    def test_004_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: * Entered numbers are displayed in the 'CVV' field
        EXPECTED: * 'DEPOSIT & PLACE BET' button is disabled (becomes enabled when 3 digits are entered)
        """
        pass

    def test_005_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'CVV' field
        """
        pass

    def test_006_enter_value_more_than_max_allowed_value_in_cvv_field(self):
        """
        DESCRIPTION: Enter value more than max allowed value in 'CVV' field
        EXPECTED: * It is impossible to enter more than 3 digits in 'CVV' field.
        """
        pass

    def test_007_tap_any_quick_stake_button_5_10_50_100(self):
        """
        DESCRIPTION: Tap any Quick Stake button
        DESCRIPTION: * 5
        DESCRIPTION: * 10
        DESCRIPTION: * 50
        DESCRIPTION: * 100
        EXPECTED: * Value in 'Deposit Amount' field is increased by chosen Quick Stake button value
        """
        pass

    def test_008_tap_plus_button_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '+' button near the deposit amount input field
        EXPECTED: The deposit amount is increased by 10 (user currency)
        """
        pass

    def test_009_focus_deposit_amount_field(self):
        """
        DESCRIPTION: Focus 'Deposit Amount' field
        EXPECTED: * 'Deposit Amount' field is focused
        EXPECTED: * Numeric keyboard is opened
        EXPECTED: * 'Quick Stakes' buttons are NOT shown
        EXPECTED: * 'DEPOSIT & PLACE BET' button is enabled if CVV is populated with 3 digits
        """
        pass

    def test_010_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: * Last entered symbol is deleted from 'Deposit Amount' field
        EXPECTED: *  '.' button on keyboard is greyed out (disabled) after removing the last digit of value (e.g. XX.X*X*)
        EXPECTED: *  '.' button on keyboard becomes enabled once ".X" value is removed  (e.g. XX*.X*)
        """
        pass

    def test_011_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: * Entered numbers are displayed in the 'Deposit Amount' field
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes enabled
        """
        pass

    def test_012_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: * 'Deposit Amount' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        EXPECTED: * '.' button becomes greyed out (disabled) on keyboard
        """
        pass

    def test_013_enter_value_more_than_max_allowed_value_in_deposit_amount_field(self):
        """
        DESCRIPTION: Enter value more than max allowed value in 'Deposit Amount' field
        EXPECTED: * It is impossible to enter more than 7 digits and 2 decimal:
        EXPECTED: e.g. "XXXXXXX.XX"
        """
        pass

    def test_014_tap_anywhere_outside_the_deposit_amount_and_cvv_field_within_quick_bet(self):
        """
        DESCRIPTION: Tap anywhere outside the 'Deposit Amount' and 'CVV' field within Quick Bet
        EXPECTED: Numeric keyboard is NOT shown and 'Deposit Amount' field still stays in focus
        """
        pass

    def test_015_tap_return_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Return' button on numeric keyboard
        EXPECTED: * 'Amount' field is NOT focused
        EXPECTED: * Numeric keyboard is NOT shown
        EXPECTED: * All fields remain populated
        """
        pass

    def test_016_set_cursor_over_deposit_amount_field_again(self):
        """
        DESCRIPTION: Set cursor over 'Deposit Amount' field again
        EXPECTED: * Selected field is focused
        EXPECTED: * Numeric keyboard is shown
        EXPECTED: *  '<currency symbol> amount value' remains shown within 'Amount' box
        EXPECTED: *  When user enters new value > new value is shown instead of an old one
        EXPECTED: *  When user taps 'Remove' on keyboard > each digit is removed one by one
        """
        pass

    def test_017_tap___button_near_the_deposit_amount_input_field(self):
        """
        DESCRIPTION: Tap '-' button near the deposit amount input field
        EXPECTED: The deposit amount is decreased by 10 (user currency)
        """
        pass

    def test_018_tap___button_till_the_field_becomes_empty(self):
        """
        DESCRIPTION: Tap '-' button till the field becomes empty
        EXPECTED: * The deposit amount field becomes empty
        EXPECTED: * Any time when value lower than 15 is inserted into input field the '-' button will clear the input field
        """
        pass

    def test_019_log_in_and_repeat_steps_1_14_for_all_currencies_gbpusd_eur_sek(self):
        """
        DESCRIPTION: Log in and repeat steps #1-14 for all currencies ('GBP','USD', 'EUR', 'SEK')
        EXPECTED: Results are the same
        """
        pass
