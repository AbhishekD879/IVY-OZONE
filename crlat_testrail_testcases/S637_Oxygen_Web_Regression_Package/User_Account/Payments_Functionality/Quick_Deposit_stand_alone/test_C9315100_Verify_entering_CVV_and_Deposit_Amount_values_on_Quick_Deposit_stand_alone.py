import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C9315100_Verify_entering_CVV_and_Deposit_Amount_values_on_Quick_Deposit_stand_alone(Common):
    """
    TR_ID: C9315100
    NAME: Verify entering 'CVV' and 'Deposit Amount' values on 'Quick Deposit' stand alone
    DESCRIPTION: This test case verifies entering stake value in a 'CVV' and 'Deposit Amount' fields using numeric keyboard for 'Quick Deposit' stand alone
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile: C16706458
    PRECONDITIONS: 1. Application is loaded
    PRECONDITIONS: 2. User with credit cards added is logged into an app
    PRECONDITIONS: 3. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_set_focus_on_cvv_field(self):
        """
        DESCRIPTION: Set focus on 'CVV' field
        EXPECTED: - 'CVV' field is focused
        EXPECTED: - Numeric keyboard is opened with '.' button disabled
        EXPECTED: - Quick Stakes buttons are NOT shown on keyboard
        EXPECTED: - 'Deposit' button is disabled
        """
        pass

    def test_002_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: - Entered numbers are displayed in the 'CVV' field
        EXPECTED: - 'Deposit' button is enabled
        """
        pass

    def test_003_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: Last entered symbol is deleted from 'CVV' field
        """
        pass

    def test_004_enter_value_more_than_max_allowed_value_in_cvv_field(self):
        """
        DESCRIPTION: Enter value more than max allowed value in 'CVV' field
        EXPECTED: It is impossible to enter more than 3 digits in 'CVV' field
        """
        pass

    def test_005_set_focus_on_deposit_amount_field(self):
        """
        DESCRIPTION: Set focus on 'Deposit Amount' field
        EXPECTED: - Numeric keyboard remains opened without Quick Stakes buttons
        EXPECTED: - 'CVV' field is unfocused
        EXPECTED: - 'Deposit Amount' field is focused
        EXPECTED: -  '.' button becomes enabled
        """
        pass

    def test_006_enter_numeric_values(self):
        """
        DESCRIPTION: Enter numeric values
        EXPECTED: - Entered numbers are displayed in the 'Deposit Amount' field
        EXPECTED: - 'Deposit' button becomes enabled once input is equal or higher than '0.01'
        """
        pass

    def test_007_tap_remove_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: Tap 'Remove' button on numeric keyboard
        EXPECTED: - Last entered symbol is deleted from 'Deposit Amount' field
        """
        pass

    def test_008_enter_value_under_1_in_decimal_format(self):
        """
        DESCRIPTION: Enter value under 1 in decimal format
        EXPECTED: - 'Amount' field is automatically filled value in decimal format (e.g. '.2 = 0.2')
        EXPECTED: - '.' button becomes greyed out (disabled) on keyboard
        """
        pass

    def test_009_enter_value_more_than_max_allowed_value_in_amount_field(self):
        """
        DESCRIPTION: Enter value more than max allowed value in 'Amount' field
        EXPECTED: It is impossible to enter more than 7 digits and 2 decimal: e.g. "XXXXXXX.XX"
        """
        pass

    def test_010___set_cursor_anywhere_within_the_quick_deposit_sectionor__tap_enter_button_on_numeric_keyboard(self):
        """
        DESCRIPTION: - Set cursor anywhere within the 'Quick Deposit' section
        DESCRIPTION: or
        DESCRIPTION: - Tap 'Enter' button on numeric keyboard
        EXPECTED: - 'Deposit Amount' field is NOT focused
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - All fields remain populated
        """
        pass

    def test_011_tap_within_the_deposit_amount_field_again(self):
        """
        DESCRIPTION: Tap within the 'Deposit Amount' field again
        EXPECTED: - Selected field is focused
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: - Quick Stakes buttons are NOT shown on keyboard
        EXPECTED: - '<currency symbol> amount value' remains shown within 'Deposit Amount' field
        EXPECTED: - When user enters new value > new value is shown instead of an old one
        EXPECTED: - When user taps 'Remove' on keyboard > each digit is removed one by one
        """
        pass

    def test_012_repeat_steps_1_11_for_all_currencies_gbpusdeur(self):
        """
        DESCRIPTION: Repeat steps #1-11 for all currencies ('GBP','USD','EUR')
        EXPECTED: 
        """
        pass
