import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C862259_Verify_validation_errors_for_CVV_and_Amount_fields(Common):
    """
    TR_ID: C862259
    NAME: Verify validation errors for 'CVV' and 'Amount' fields
    DESCRIPTION: This test case verifies validation errors for 'CVV' and 'Amount' fields
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in
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

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
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
        EXPECTED: * 'QUICK DEPOSIT' section is displayed instead of Quick Bet
        EXPECTED: * 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        EXPECTED: * 'Deposit Amount' field is pre-populated automatically with difference between entered stake value and users balance
        EXPECTED: * '-' and '+' buttons are displayed on both sides of deposit amount input field
        """
        pass

    def test_005_enter_less_than_3_digits_in_cvv_field(self):
        """
        DESCRIPTION: Enter less than 3 digits in 'CVV' field
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes enabled
        EXPECTED: * 'CVV' field is populated with value
        """
        pass

    def test_006_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET' button
        EXPECTED: * 'Your CV2 is incorrect.' validation message is displayed below 'CVV' field
        EXPECTED: * Deposit is unsuccessful
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'CVV' and 'Deposit Amount' fields are NOT cleared
        """
        pass

    def test_007_enter_correct_value_in_cvv_field_clear_deposit_amount_field_and_enter_value_less_than_5(self):
        """
        DESCRIPTION: Enter correct value in 'CVV' field, clear 'Deposit Amount' field and enter value less than 5
        EXPECTED: * 'DEPOSIT & PLACE BET' button becomes enabled
        EXPECTED: * 'CVV' and 'Deposit Amount' fields are populated with values
        """
        pass

    def test_008_tap_deposit__place_bet__button(self):
        """
        DESCRIPTION: Tap 'DEPOSIT & PLACE BET'  button
        EXPECTED: * 'The minimum deposit amount is <currency symbol>5.' validation message is displayed below 'Deposit Amount' field
        EXPECTED: * Deposit is unsuccessful
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'CVV' and 'Deposit Amount' fields are NOT cleared
        EXPECTED: where <currency symbol> - currency that was set during registration
        """
        pass
