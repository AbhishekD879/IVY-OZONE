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
class Test_C1924744_Verify_Unsuccessful_Depositing_via_PayPal_via_already_registered_PayPal_Account(Common):
    """
    TR_ID: C1924744
    NAME: Verify Unsuccessful Depositing via PayPal via already registered PayPal Account
    DESCRIPTION: This test case verifies Unsuccessful Depositing via PayPal via already registered PayPal Account.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-1952 (Use "Message" part of responses within the cashier)
    DESCRIPTION: *   BMA-5618 (Default Error message for Cashier functionality)
    DESCRIPTION: *   BMA-6950 cashier tabs (deposit page) name change
    PRECONDITIONS: *  In CMS > System Configuration > 'Pay Pal' section > 'viaSafeCharge' check box is NOT checked
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has a valid (unrestricted) PayPal account from which his/her **CAN NOT** deposit funds via (UAT team - to provide)
    PRECONDITIONS: Available PayPal Accounts:
    PRECONDITIONS: *   ppone@yopmail.com / devine12
    PRECONDITIONS: *   pptwo@yopmail.com / devine12
    PRECONDITIONS: *   ppthree@yopmail.com / devine12
    PRECONDITIONS: *   ppfour@yopmail.com / devine12
    PRECONDITIONS: *   ppfive@yopmail.com / devine12
    PRECONDITIONS: NOTE: in case server returns unexpected response: only error code (no “message”, “errorMessage”…)/empty response/ other data structure default error message should be displyed: "**There has been an error with your transaction. Please contact our Customer Services team.**"
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
        EXPECTED: *   'Add PayPal' tab is opened
        EXPECTED: *   Registered PayPal account is available
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
        EXPECTED: Pop-up  is shown:
        EXPECTED: *   header "Redirecting"
        EXPECTED: *   body "Redirecting to PayPal"
        EXPECTED: *   Loading spinner
        """
        pass

    def test_006_submit_paypal_page(self):
        """
        DESCRIPTION: Submit PayPal page
        EXPECTED: 
        """
        pass

    def test_007_provoke_situation_when_transaction_is_impossibleeg_account_is_frozen_not_enough_balance(self):
        """
        DESCRIPTION: Provoke situation when transaction is impossible
        DESCRIPTION: (e.g. account is frozen, not enough balance)
        EXPECTED: 
        """
        pass

    def test_008_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: *   User is stayed on 'Add PayPal' tab
        EXPECTED: *   Check message in WebSockets. The "**message**" part of the error response is shown. (e.g. "We are sorry, but your PayPal deposit has been declined. Please try another credit card. Good luck and sorry for any inconvenience caused.")
        EXPECTED: Note: If "message" part is absent, "errorMessage"/"description"/"errorDescription" part is shown (next available value in mentioned order)
        """
        pass

    def test_009_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is NOT changed on an amount set on step №4
        """
        pass
