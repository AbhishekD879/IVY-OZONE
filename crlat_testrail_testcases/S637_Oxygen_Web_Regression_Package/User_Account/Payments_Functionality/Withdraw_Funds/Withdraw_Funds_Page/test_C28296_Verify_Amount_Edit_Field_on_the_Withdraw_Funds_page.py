import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28296_Verify_Amount_Edit_Field_on_the_Withdraw_Funds_page(Common):
    """
    TR_ID: C28296
    NAME: Verify Amount Edit Field on the Withdraw Funds page
    DESCRIPTION: This test case verifies Amount Edit Field on the Withdraw Funds page
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has at least one registered Payment Method
    PRECONDITIONS: JIRA tickets:
    PRECONDITIONS: BMA-9157 Apply numerical keyboard
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_menu_item(self):
        """
        DESCRIPTION: Tap 'Withdraw' menu item
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered cards is shown
        EXPECTED: * Payment Method is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_003_select_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select Payment Method from drop-down
        EXPECTED: 
        """
        pass

    def test_004_verify_amount_edit_field(self):
        """
        DESCRIPTION: Verify amount edit field
        EXPECTED: *   'Enter Amount Manually...' text is displayed by default
        EXPECTED: *   Amount edit field is required
        """
        pass

    def test_005_tap_enter_amount_field(self):
        """
        DESCRIPTION: Tap Enter amount field
        EXPECTED: Numeric keypad is opened (on devices)
        """
        pass

    def test_006_enter_letters_into_amount_edit_field(self):
        """
        DESCRIPTION: Enter letters into amount edit field
        EXPECTED: It is not allowed
        """
        pass

    def test_007_enter_symbols_into_amount_edit_field(self):
        """
        DESCRIPTION: Enter symbols into amount edit field
        EXPECTED: It is not allowed
        """
        pass

    def test_008_verify_max_amount(self):
        """
        DESCRIPTION: Verify max amount
        EXPECTED: Max number of digits is 7 and 2 decimal:
        EXPECTED: e.g. "XXXXXXX.XX"
        """
        pass

    def test_009_enter_amount_less_than_5_into_amount_edit_field_and_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Enter amount less than 5 into amount edit field and tap 'Withdraw Funds' button
        EXPECTED: *   Error message is shown: "**The minimum withdraw amount is <currency symbol>5**"
        EXPECTED: *   Entered value is not cleared
        """
        pass

    def test_010_enter_decimal_valuetest_data_105(self):
        """
        DESCRIPTION: Enter decimal value
        DESCRIPTION: Test data: 10.5
        EXPECTED: Value is accepted
        """
        pass
