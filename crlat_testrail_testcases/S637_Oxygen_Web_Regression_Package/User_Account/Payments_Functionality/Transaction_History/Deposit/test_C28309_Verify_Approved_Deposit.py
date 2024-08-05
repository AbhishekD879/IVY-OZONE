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
class Test_C28309_Verify_Approved_Deposit(Common):
    """
    TR_ID: C28309
    NAME: Verify Approved Deposit
    DESCRIPTION: This test case verifies Approved Deposit.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: *   [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has registered Debit/Credit Card, PayPal and NETELLER methods
    PRECONDITIONS: *   Balance of account is enough for Depositing with.
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open Deposit Page
        EXPECTED: *   'Deposit' page is opened
        EXPECTED: *   Drop-down list with existing registered Payment Methods is shown
        """
        pass

    def test_002_select_debitcredit_card(self):
        """
        DESCRIPTION: Select Debit/Credit Card
        EXPECTED: 
        """
        pass

    def test_003_fill_in_all_required_fields_with_valid_data(self):
        """
        DESCRIPTION: Fill in all required fields with valid data
        EXPECTED: 
        """
        pass

    def test_004_enter_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_005_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: *   Successfull message: **"Your deposit of <currency symbol> XX.XX was successful."** is shown
        EXPECTED: *   User stays on the 'Registered' tab
        """
        pass

    def test_006_go_to_my_account___transaction_history_page(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Transaction History' page
        EXPECTED: *   'Transactions' tab on 'Account History' page is opened
        EXPECTED: *   'Deposit' button and 'Approved' tab are selected by default
        """
        pass

    def test_007_check_approved_tab(self):
        """
        DESCRIPTION: Check 'Approved' tab
        EXPECTED: Made deposit transaction on previous steps is displayed (at the top of the list)
        """
        pass

    def test_008_verify_approved_transaction_info(self):
        """
        DESCRIPTION: Verify approved transaction info
        EXPECTED: 3 columns are displayed:
        EXPECTED: *   **Type of payment method**
        EXPECTED: *   **'Date/Time:' **label, date of deposit in format: DD-MM-YYYY  HH:MM (24-hour clock) and card number in format: '**\**\*|\* <the last 4 digits of the used card>**'
        EXPECTED: *   **'Amount:'** label and value of deposit with **<currency symbol>**
        """
        pass

    def test_009_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_010_make_deposit_via_paypal_method_from_deposit_methods_or_add_paypal_tab(self):
        """
        DESCRIPTION: Make deposit via PayPal method from 'Deposit Methods' or 'Add PayPal' tab
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_7_9(self):
        """
        DESCRIPTION: Repeat steps №7-9
        EXPECTED: 
        """
        pass

    def test_012_go_to_deposit_page(self):
        """
        DESCRIPTION: Go to 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_013_make_deposit_via_neteller_method_from_deposit_methods_or_add_neteller_tab(self):
        """
        DESCRIPTION: Make deposit via NETELLER method from 'Deposit Methods' or 'Add NETELLER' tab
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_7_9(self):
        """
        DESCRIPTION: Repeat steps №7-9
        EXPECTED: 
        """
        pass
