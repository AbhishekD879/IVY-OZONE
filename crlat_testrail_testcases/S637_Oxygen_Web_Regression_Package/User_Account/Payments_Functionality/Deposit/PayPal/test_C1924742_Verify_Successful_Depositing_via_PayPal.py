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
class Test_C1924742_Verify_Successful_Depositing_via_PayPal(Common):
    """
    TR_ID: C1924742
    NAME: Verify Successful Depositing via PayPal
    DESCRIPTION: This test case verifies Successful Depositing functionality via PayPal.
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
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * It's better to create a new user and add PayPal for him than trying to add PayPal to an existing user.
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown
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

    def test_004_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: *   Amount is displayed in Amount edit field
        EXPECTED: *   'Deposit' button is enabled
        """
        pass

    def test_005_verify_pop_up(self):
        """
        DESCRIPTION: Verify pop-up
        EXPECTED: Pop-up is shown:
        EXPECTED: *   header "Redirecting"
        EXPECTED: *   body "Redirecting to PayPal"
        EXPECTED: *   Loading spinner
        """
        pass

    def test_006_submit_paypal_form(self):
        """
        DESCRIPTION: Submit PayPal form
        EXPECTED: 
        """
        pass

    def test_007_tap_pay_now_button(self):
        """
        DESCRIPTION: Tap 'Pay Now' button
        EXPECTED: *   User is redirected to 'My Payments' tab
        EXPECTED: *   Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"**
        EXPECTED: *   Amount on message is displayed in decimal format
        """
        pass

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is increased on amount set on step №4
        """
        pass

    def test_009_verify_drop_down_list(self):
        """
        DESCRIPTION: Verify drop-down list
        EXPECTED: PayPal payment method is shown at the top of the registered payments drop down list in format:
        EXPECTED: **"PayPal (email@address.com)"**
        """
        pass

    def test_010_tap_add_paypal_tab(self):
        """
        DESCRIPTION: Tap 'Add PayPal' tab
        EXPECTED: 'Add PayPal' tab is selected
        """
        pass

    def test_011_verify_registered_paypal_account(self):
        """
        DESCRIPTION: Verify registered PayPal account
        EXPECTED: The following info is shown at the top of the PayPal page:
        EXPECTED: **Your Registered PayPal Account:**
        EXPECTED: **"email@address.com"**
        """
        pass

    def test_012_verify_quick_deposit_buttons(self):
        """
        DESCRIPTION: Verify quick deposit buttons
        EXPECTED: 1.  Quick deposit buttons are displayed below the** 'Add Amount':** label
        EXPECTED: 2.  The following values are shown:
        EXPECTED: *   +5
        EXPECTED: *   +10
        EXPECTED: *   +20
        EXPECTED: *   +50
        EXPECTED: *   +100
        """
        pass

    def test_013_verify_enteramountedit_field(self):
        """
        DESCRIPTION: Verify '**Enter** **Amount:'** edit field
        EXPECTED: Amount edit field is required and located below the quick deposit buttons
        """
        pass

    def test_014_verify_deposit_button(self):
        """
        DESCRIPTION: Verify 'Deposit' button
        EXPECTED: 'Deposit' button is enabled by default
        """
        pass
