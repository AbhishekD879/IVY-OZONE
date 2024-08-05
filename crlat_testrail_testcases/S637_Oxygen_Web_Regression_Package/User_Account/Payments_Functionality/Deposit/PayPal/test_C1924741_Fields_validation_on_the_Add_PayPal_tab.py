import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C1924741_Fields_validation_on_the_Add_PayPal_tab(Common):
    """
    TR_ID: C1924741
    NAME: Fields validation on the 'Add PayPal' tab
    DESCRIPTION: This test case verifies fields validation on the 'Add PayPal' tab.
    PRECONDITIONS: JIRA tickets:
    PRECONDITIONS: BMA-9157 Apply numerical keyboard
    PRECONDITIONS: BMA-6950 cashier tabs (deposit page) name change
    PRECONDITIONS: *  In CMS > System Configuration > 'Pay Pal' section > 'viaSafeCharge' check box is NOT checked
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has a valid (unrestricted) PayPal account from which his/her can deposit funds via
    PRECONDITIONS: *   Balance is enough for deposit from
    PRECONDITIONS: Available PayPal Accounts:
    PRECONDITIONS: *   ppone@yopmail.com / devine12
    PRECONDITIONS: *   pptwo@yopmail.com / devine12
    PRECONDITIONS: *   ppthree@yopmail.com / devine12
    PRECONDITIONS: *   ppfour@yopmail.com / devine12
    PRECONDITIONS: *   ppfive@yopmail.com / devine12
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_deposit_button_at_the_top_of_the_right_menu_or_on_the_betslip_page(self):
        """
        DESCRIPTION: Tap 'Deposit' button at the top of the Right menu or on the Betslip page
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   'My Payments' tab is selected by default
        """
        pass

    def test_003_tap_add_paypal_tab(self):
        """
        DESCRIPTION: Tap 'Add PayPal' tab
        EXPECTED: 'Add PayPal' tab is selected
        """
        pass

    def test_004_verify_quick_deposit_buttons(self):
        """
        DESCRIPTION: Verify quick deposit buttons
        EXPECTED: *   Buttons work in a cumulative way (e.g. tap '10' and tap '20' - the amount would be '30')
        EXPECTED: *   Set value is shown in Amount edit field
        """
        pass

    def test_005_verify_amountedit_field(self):
        """
        DESCRIPTION: Verify Amount edit field
        EXPECTED: *   Amount edit field is mandatory and empty by default
        EXPECTED: *   Only numeric values and '.' are accepted
        EXPECTED: *   **Numeric keyboard** is opened (for mobile devices) when cursor is set in the text input field
        """
        pass

    def test_006_verify_max_amount(self):
        """
        DESCRIPTION: Verify max amount
        EXPECTED: Max number of digits is 7 and 2 decimal:
        EXPECTED: e.g. "XXXXXXX.XX"
        """
        pass

    def test_007_enter_less_than_5_into_amount_edit_field_and_tap_deposit_button(self):
        """
        DESCRIPTION: Enter less than 5 into amount edit field and tap 'Deposit' button
        EXPECTED: *   Error message is shown: ​**"The minimum deposit amount is <currency symbol> 5"**
        EXPECTED: *   Entered valued is not cleared
        """
        pass
