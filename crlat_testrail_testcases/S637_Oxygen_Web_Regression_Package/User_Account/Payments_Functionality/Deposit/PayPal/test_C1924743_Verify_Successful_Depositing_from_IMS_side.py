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
class Test_C1924743_Verify_Successful_Depositing_from_IMS_side(Common):
    """
    TR_ID: C1924743
    NAME: Verify Successful Depositing from IMS side
    DESCRIPTION: This test case verifies Successful Depositing functionality via PayPal from IMS side.
    PRECONDITIONS: *  In CMS > System Configuration > 'Pay Pal' section > 'viaSafeCharge' check box is NOT checked
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has a valid PayPal account from which they can deposit funds from
    PRECONDITIONS: *   Balance is enough for deposit from
    PRECONDITIONS: Accounts:
    PRECONDITIONS: ppone@yopmail.com / devine12
    PRECONDITIONS: pptwo@yopmail.com / devine12
    PRECONDITIONS: ppthree@yopmail.com / devine12
    PRECONDITIONS: ppfour@yopmail.com / devine12
    PRECONDITIONS: Link and credentials to IMS are here: https://confluence.egalacoral.com/display/MOB/Playtech+IMS
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
        EXPECTED: * Amount is displayed in Amount edit field
        EXPECTED: * 'Deposit' button is enabled
        """
        pass

    def test_005_verify_pop_up(self):
        """
        DESCRIPTION: Verify pop-up
        EXPECTED: Pop-up is shown:
        EXPECTED: * header "Redirecting"
        EXPECTED: * body "Redirecting to PayPal"
        EXPECTED: * Loading spinner
        """
        pass

    def test_006_submit_paypal_form(self):
        """
        DESCRIPTION: Submit PayPal form
        EXPECTED: *   Amount is displayed in Amount edit field
        EXPECTED: *   'Deposit' button is enabled
        """
        pass

    def test_007_tap_pay_now_button(self):
        """
        DESCRIPTION: Tap 'Pay Now' button
        EXPECTED: * User is redirected to 'My Payments' tab
        EXPECTED: * Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"**
        EXPECTED: * Amount on message is displayed in decimal format
        """
        pass

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is increased on amount set on step №4
        """
        pass

    def test_009_find_the_user_in_ims_using_player_search(self):
        """
        DESCRIPTION: Find the user in IMS using Player search
        EXPECTED: User is found
        """
        pass

    def test_010_verify_transaction_information_of_created_record_in_the_transactions_table(self):
        """
        DESCRIPTION: Verify Transaction Information of created record (in the "Transactions" table)
        EXPECTED: All data in the corresponding table row is correct
        """
        pass
