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
class Test_C28314_Verify_Declined_Withdrawal(Common):
    """
    TR_ID: C28314
    NAME: Verify Declined Withdrawal
    DESCRIPTION: This test case verifies Declined Withdrawal.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered Debit/Credit Card, PayPal and NETELLER methods
    PRECONDITIONS: *   Balance of account is enough for withdraw from
    PRECONDITIONS: Playtech IMS links and credentials can be found here: https://confluence.egalacoral.com/display/SPI/Playtech+IMS
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_withdraw_button(self):
        """
        DESCRIPTION: Tap 'Withdraw' button
        EXPECTED: *   'Withdraw Funds' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        """
        pass

    def test_003_select_debitcredit_card(self):
        """
        DESCRIPTION: Select Debit/Credit card
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_005_tap_withdraw_funds_button(self):
        """
        DESCRIPTION: Tap 'Withdraw Funds' button
        EXPECTED: *   Successfull message: **"Your withdrawal request has been successful.Reference: #XXXXXXX"** *(ID of successful response )** is shown
        EXPECTED: *   User stays on the 'Withdraw Funds' page (refreshed with clear form)
        """
        pass

    def test_006_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is decremented on amount set on step №4
        """
        pass

    def test_007_go_to_my_account___transaction_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Transaction History' page
        EXPECTED: *   'Transactions' tab on 'Account History' page is opened
        EXPECTED: *   'Deposit' button is selected by default
        """
        pass

    def test_008_tap_withdraw_button___pending_tab(self):
        """
        DESCRIPTION: Tap 'Withdraw' button -> 'Pending' tab
        EXPECTED: Made withdrawal transaction on previous steps is displayed
        """
        pass

    def test_009_go_to_ims_and_decline_this_transaction(self):
        """
        DESCRIPTION: Go to IMS and **decline **this transaction
        EXPECTED: 
        """
        pass

    def test_010_tap_refresh_button_on_the_pending_tab(self):
        """
        DESCRIPTION: Tap 'Refresh' button on the 'Pending' tab
        EXPECTED: Verified withdrawal transaction disappears
        """
        pass

    def test_011_tap_decline_tab(self):
        """
        DESCRIPTION: Tap 'Decline' tab
        EXPECTED: Withdrawal transaction from step №7 appears on the 'Decline' tab
        """
        pass

    def test_012_verify_declined_transaction_info(self):
        """
        DESCRIPTION: Verify declined transaction info
        EXPECTED: 3 columns are displayed:
        EXPECTED: *   **Type of payment method**
        EXPECTED: *   **'Date:' **label, date of withdrawal in format: DD-MM-YYYY  HH:MM (24-hour clock) and card number in format: '\**\*|\* **<the last 4 digits of the **used** card>**'
        EXPECTED: *   **'Amount:'** label and value of withdrawal with **<currency symbol>**
        """
        pass

    def test_013_go_to_withdraw_funds_page(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page
        EXPECTED: 
        """
        pass

    def test_014_select_paypal_method(self):
        """
        DESCRIPTION: Select PayPal method
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_4_12(self):
        """
        DESCRIPTION: Repeat steps №4-12
        EXPECTED: 
        """
        pass

    def test_016_go_to_withdraw_funds_page(self):
        """
        DESCRIPTION: Go to 'Withdraw Funds' page
        EXPECTED: 
        """
        pass

    def test_017_select_neteller_method(self):
        """
        DESCRIPTION: Select NETELLER method
        EXPECTED: 
        """
        pass

    def test_018_repeat_steps_4_12(self):
        """
        DESCRIPTION: Repeat steps №4-12
        EXPECTED: 
        """
        pass
