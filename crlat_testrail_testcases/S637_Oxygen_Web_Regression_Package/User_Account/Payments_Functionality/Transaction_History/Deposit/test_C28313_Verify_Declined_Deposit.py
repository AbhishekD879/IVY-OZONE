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
class Test_C28313_Verify_Declined_Deposit(Common):
    """
    TR_ID: C28313
    NAME: Verify Declined Deposit
    DESCRIPTION: This test case verifies Declined Deposit.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered Debit/Credit Card, PayPal and NETELLER methods
    PRECONDITIONS: *   Card balance is **NOT **enough for Depositing with (e.g. user: Christina, pass: qwerty).
    """
    keep_browser_open = True

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_002_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        """
        pass

    def test_003_select_debitcredit_card_without_enough_balance_for_depositing(self):
        """
        DESCRIPTION: Select Debit/Credit card without enough balance for depositing
        EXPECTED: 
        """
        pass

    def test_004_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_005_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_006_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: *   Error message: **"1013: Canceled by the Payment Method Processor"** is shown
        EXPECTED: *   User stays on the 'Registered' tab
        """
        pass

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is not updated
        """
        pass

    def test_008_go_to_my_account___transaction_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Transaction History' page
        EXPECTED: *   'Transactions' tab on 'Account History' page is opened
        EXPECTED: *   'Deposit' button and 'Approved' tab are selected by default
        """
        pass

    def test_009_tap_declined_tab(self):
        """
        DESCRIPTION: Tap 'Declined' tab
        EXPECTED: Made deposit transaction on previous steps is displayed (at the top of the list)
        """
        pass

    def test_010_verify_declined_transaction_info(self):
        """
        DESCRIPTION: Verify declined transaction info
        EXPECTED: 3 columns are displayed:
        EXPECTED: *   **Type of payment method**
        EXPECTED: *   **'Date:' **label, date of deposit in format: DD-MM-YYYY  HH:MM (24-hour clock) and card number in format: '\**\*|\* **<the last 4 digits of the **used** card>**'
        EXPECTED: *   **'Amount:'** label and value of deposit with **<currency symbol>**
        """
        pass

    def test_011_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_012_select_paypal_method_without_enough_balance_for_depositing(self):
        """
        DESCRIPTION: Select PayPal method without enough balance for depositing
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_4_10(self):
        """
        DESCRIPTION: Repeat steps №4-10
        EXPECTED: 
        """
        pass

    def test_014_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_015_select_neteller_method_wthout_enough_balance_for_depositing(self):
        """
        DESCRIPTION: Select NETELLER method wthout enough balance for depositing
        EXPECTED: 
        """
        pass

    def test_016_repeat_steps_4_10(self):
        """
        DESCRIPTION: Repeat steps №4-10
        EXPECTED: 
        """
        pass
