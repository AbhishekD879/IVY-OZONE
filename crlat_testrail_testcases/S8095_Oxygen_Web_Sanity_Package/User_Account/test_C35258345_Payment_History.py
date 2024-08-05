import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C35258345_Payment_History(Common):
    """
    TR_ID: C35258345
    NAME: Payment History
    DESCRIPTION: This test case verifies Payment History page.
    PRECONDITIONS: 1 User is logged in to view their Payment History
    PRECONDITIONS: 2 User has Approved and Declined Deposit transactions for the past three months
    PRECONDITIONS: 3 User has Approved/Pending/Declined Withdraw transactions for the past three months (optional)
    PRECONDITIONS: 4 User has navigated to the  'My Account' menu
    """
    keep_browser_open = True

    def test_001_select_banking__balances__payment_historycoral_history__payment_history(self):
        """
        DESCRIPTION: Select 'Banking & Balances' > 'Payment History'
        DESCRIPTION: (Coral: History > Payment History)
        EXPECTED: * 'Payment History' page is opened
        EXPECTED: ![](index.php?/attachments/get/111269030)
        """
        pass

    def test_002_specify_dates_click_goverify_transaction_history_table_under_the_filter(self):
        """
        DESCRIPTION: Specify dates, Click 'GO',
        DESCRIPTION: Verify transaction history table under the filter
        EXPECTED: Table consists of:
        EXPECTED: 'Date' column
        EXPECTED: 'Transaction type' column
        EXPECTED: 'Transaction amount' column
        EXPECTED: transaction block is expandable
        """
        pass

    def test_003_try_different_values_in_the_filter_and_check_the_table(self):
        """
        DESCRIPTION: Try different values in the filter and check the table
        EXPECTED: Table is shown according to the filter settings
        """
        pass

    def test_004_expand_a_few_transactions_to_verify_details(self):
        """
        DESCRIPTION: Expand a few transactions to verify details
        EXPECTED: Expanded area contains following information:
        EXPECTED: Time
        EXPECTED: Product
        EXPECTED: Balance
        EXPECTED: Transaction ID
        EXPECTED: Explained type of transaction (not for all transactions, if possible check for:
        EXPECTED: - withdrawal,
        EXPECTED: - redeem promotions)
        """
        pass

    def test_005_verify_net_deposits_value_correctness(self):
        """
        DESCRIPTION: Verify 'Net Deposits' value correctness
        EXPECTED: Net deposits value equals to total of all deposits minus the sum of all withdrawals for the whole time
        """
        pass

    def test_006_make_a_deposit_and_verify_the_values_in_the_table_change(self):
        """
        DESCRIPTION: Make a deposit and verify the values in the table change
        EXPECTED: The values change accordingly
        """
        pass

    def test_007_tap_on_the__icon_near_net_deposits(self):
        """
        DESCRIPTION: Tap on the '?' icon near Net Deposits
        EXPECTED: pop-up is shown:
        EXPECTED: "Net deposits are calculated by taking the sum of approved deposits (including any deposit corrections) and deducting approved withdrawals (including any withdrawal corrections)."
        EXPECTED: ![](index.php?/attachments/get/111269031)
        """
        pass
