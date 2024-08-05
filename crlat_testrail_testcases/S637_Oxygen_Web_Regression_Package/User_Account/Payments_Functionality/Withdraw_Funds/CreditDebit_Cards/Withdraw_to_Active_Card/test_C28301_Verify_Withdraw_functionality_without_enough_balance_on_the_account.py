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
class Test_C28301_Verify_Withdraw_functionality_without_enough_balance_on_the_account(Common):
    """
    TR_ID: C28301
    NAME: Verify Withdraw functionality without enough balance on the account
    DESCRIPTION: This test case verifies Withdraw functionality without enough balance on the account.
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-1952 (Use "Message" part of responses within the cashier)
    DESCRIPTION: *   BMA-5618 (Default Error message for Cashier functionality)
    PRECONDITIONS: User has two accounts:
    PRECONDITIONS: 1.  First: with positive balance and added cards
    PRECONDITIONS: 2.  Second: with card added to account, but without money deposited from it
    PRECONDITIONS: NOTE: in case server returns unexpected response: only error code (no “message”, “errorMessage”…)/empty response/ other data structure default error message should be displyed: "**There has been an error with your transaction. Please contact our Customer Services team.**"
    """
    keep_browser_open = True

    def test_001_log_into_the_first_account_from_preconditions(self):
        """
        DESCRIPTION: Log into the first account from Preconditions
        EXPECTED: User is successfully logged in
        """
        pass

    def test_002_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_003_tap_withdraw_button(self):
        """
        DESCRIPTION: Tap 'Withdraw' button
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        EXPECTED: *   Drop-down is collapsed by default
        """
        pass

    def test_004_select_creditdebit_cards_from_drop_down(self):
        """
        DESCRIPTION: Select Credit/Debit Cards from drop-down
        EXPECTED: 
        """
        pass

    def test_005_enter_amountbigger_than_current_balance_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount bigger than current balance manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_006_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Check message in WebSockets. The "**message**" part of the error response is shown (e.g. "message":"The amount you wish to withdraw exceeds your current account balance.")
        EXPECTED: Note: If "message" part is absent, "errorMessage"/"description"/"errorDescription" part is shown (next available value in mentioned order)
        EXPECTED: *   User stays on the 'Withdraw Funds' page
        EXPECTED: *   User Balance is not changed
        EXPECTED: *   Entered amount is not cleared
        """
        pass

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is not changed
        """
        pass

    def test_008_enter_very_big_amount_manually_or_using_quick_deposit_buttons_the_amount_which_exceed_max_limit(self):
        """
        DESCRIPTION: Enter very big amount manually or using quick deposit buttons (the amount which exceed max limit)
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_009_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Check message in WebSockets. The "**message**" part of the error response is shown. (e.g. "message":"Sorry, but the maximum amount allowed for a VISA withdrawal is $100000. Please try to withdraw a smaller amount. Thank you and good luck!")
        EXPECTED: Note: If "message" part is absent, "errorMessage"/"description"/"errorDescription" part is shown (next available value in mentioned order)
        EXPECTED: *   User stays on the 'Withdraw Funds' page
        EXPECTED: *   User balance is not changed
        EXPECTED: *   Entered amount is NOT cleared
        """
        pass

    def test_010_log_out_from_the_oxygen_application(self):
        """
        DESCRIPTION: Log out from the Oxygen application
        EXPECTED: Login Button should be visible
        """
        pass

    def test_011_log_into_the_second_account_from_preconditions(self):
        """
        DESCRIPTION: Log into the second account from Preconditions
        EXPECTED: User is successfully logged in
        """
        pass

    def test_012_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps №2-5
        EXPECTED: 
        """
        pass

    def test_013_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Check message in WebSockets. The "**message**" part of the error response is shown. (e.g. "message":"**Sorry, but in order to withdraw using <MC/VISA..> you must first make deposit using this method. Thank you.**")
        EXPECTED: *   User stays on the 'Withdraw Funds' page
        EXPECTED: *   User Balance is not changed
        EXPECTED: *   Entered amount is not cleared
        """
        pass
