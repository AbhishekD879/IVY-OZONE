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
class Test_C28311_Impossible_to_test__Verify_Pending_Deposit(Common):
    """
    TR_ID: C28311
    NAME: Impossible to test - Verify Pending Deposit
    DESCRIPTION: This test case verifies Pending Deposit.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered Debit/Credit Card, PayPal and NETELLER methods
    PRECONDITIONS: *   Balance of account is enough for Depositing with.
    PRECONDITIONS: Note: IMS does not offer this option. There is a production tool called **IOVATION**** **that can block a deposit and needs manual approval.
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
        EXPECTED: *   Drop-down list with existing reqistered Payment Methods is shown
        EXPECTED: *   Drop-down is expanded by default
        """
        pass

    def test_003_select_debitcredit_card(self):
        """
        DESCRIPTION: Select Debit/Credit card
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
        EXPECTED: *   Successfull message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"** *(ID of successfull response "ID":33015) *is shown
        EXPECTED: *   User stays on the 'Registered' tab
        """
        pass

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user Balance
        EXPECTED: User Balance is incremented on amount set on step №4
        """
        pass

    def test_008_ask_uat_team_to_make_this_transaction_pending(self):
        """
        DESCRIPTION: Ask UAT team to make this transaction Pending
        EXPECTED: 
        """
        pass

    def test_009_go_to_my_account___transaction_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Transaction History' page
        EXPECTED: *   'Transactions' tab on 'Account History' page is opened
        EXPECTED: *   'Deposit' button and 'Approved' tab are selected by default
        """
        pass

    def test_010_tap_pending_tab(self):
        """
        DESCRIPTION: Tap 'Pending' tab
        EXPECTED: *   'Pending' tab is selected
        EXPECTED: *   Made deposit transaction on previous steps is displayed (at the top of the list)
        """
        pass

    def test_011_verify_transaction_info(self):
        """
        DESCRIPTION: Verify transaction info
        EXPECTED: 3 columns are displayed:
        EXPECTED: *   **Type of payment method**
        EXPECTED: *   **'Date/Time:'** label, date of deposit in format: DD-MM-YYYY  HH:MM (24-hour clock) and card number in format: '\**\*|\* **<the last 4 digits of the used card>**'
        EXPECTED: *   **'Amount:'** label and value of deposit with <currency symbol>
        """
        pass

    def test_012_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_013_select_paypal_method(self):
        """
        DESCRIPTION: Select PayPal method
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass

    def test_015_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_016_select_neteller_method(self):
        """
        DESCRIPTION: Select NETELLER method
        EXPECTED: 
        """
        pass

    def test_017_repeat_steps_4_11(self):
        """
        DESCRIPTION: Repeat steps №4-11
        EXPECTED: 
        """
        pass
