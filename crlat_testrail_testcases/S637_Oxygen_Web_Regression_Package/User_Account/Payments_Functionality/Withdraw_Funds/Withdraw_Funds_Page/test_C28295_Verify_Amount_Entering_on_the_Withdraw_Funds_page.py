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
class Test_C28295_Verify_Amount_Entering_on_the_Withdraw_Funds_page(Common):
    """
    TR_ID: C28295
    NAME: Verify Amount Entering on the Withdraw Funds page
    DESCRIPTION: This test case verifies possibility to enter Amount on the Withdraw Funds page
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has at least one registered Payment Method
    PRECONDITIONS: JIRA tickets:
    PRECONDITIONS: BMA-9157 Apply numerical keyboard
    PRECONDITIONS: BMA-16872 (Unlimited "0" input CV2 field on Deposit and after decimal point in "Amount" field)
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
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_003_select_payment_method_from_drop_down(self):
        """
        DESCRIPTION: Select Payment Method from drop-down
        EXPECTED: 
        """
        pass

    def test_004_verify_quick_withdraw_buttons(self):
        """
        DESCRIPTION: Verify quick withdraw buttons
        EXPECTED: *   Quick withdraw buttons are displayed below the 'Withdraw Amount:' label
        EXPECTED: *   The following values are shown:
        EXPECTED: 1.  5
        EXPECTED: 2.  10
        EXPECTED: 3.  20
        EXPECTED: 4.  50
        EXPECTED: 5.  100
        """
        pass

    def test_005_verify_amount_edit_field(self):
        """
        DESCRIPTION: Verify amount edit field
        EXPECTED: *   'Enter Amount Manually...' text is displayed by default
        EXPECTED: *   Amount edit field is required and empty by default
        """
        pass

    def test_006_tap_quick_deposit_buttons_and_check_amount_edit_field(self):
        """
        DESCRIPTION: Tap quick deposit buttons and check amount edit field
        EXPECTED: *   'Enter Amount Manually...' text is not shown anymore
        EXPECTED: *   Buttons work in a cumulative way (e.g. tap '10' and tap '20' - the amount would be '30')
        EXPECTED: *   Set value is shown
        """
        pass

    def test_007_tap_amount_edit_field(self):
        """
        DESCRIPTION: Tap Amount edit field
        EXPECTED: Numeric keypad is opened (on devices)
        """
        pass

    def test_008_try_to_edit_amount_manually(self):
        """
        DESCRIPTION: Try to edit amount manually
        EXPECTED: It is allowed to edit amount set with the help of quick deposit buttons / manually
        """
        pass

    def test_009_clear_amount_edit_field(self):
        """
        DESCRIPTION: Clear amount edit field
        EXPECTED: 'Enter Amount Manually...' text is displayed
        """
        pass

    def test_010_tap_amount_edit_field(self):
        """
        DESCRIPTION: Tap Amount edit field
        EXPECTED: Numeric keypad is opened (on devices)
        """
        pass

    def test_011_enter_amount_manually__0000123_12300(self):
        """
        DESCRIPTION: Enter amount manually ( 0000123, 123.00)
        EXPECTED: *   'Enter Amount Manually...' text is not shown anymore
        EXPECTED: *   Entered value is shown
        EXPECTED: (only allows to enter 7 digits before "."
        EXPECTED: and all "0" from beginning are cropped when cursor is on other field,
        EXPECTED: only 2 digits after . is allowed
        EXPECTED: and if no digits after "." - ".00" is added at the end)
        """
        pass

    def test_012_repeat_step_9(self):
        """
        DESCRIPTION: Repeat step №9
        EXPECTED: 'Enter Amount Manually...' text is displayed
        """
        pass
