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
class Test_C59015301_Transactions_History(Common):
    """
    TR_ID: C59015301
    NAME: Transactions History
    DESCRIPTION: This test case verifies Transactions History page.
    PRECONDITIONS: 1 User is logged in to view their Payment History
    PRECONDITIONS: 2 User has Approved and Declined Deposit transactions for the past three months
    PRECONDITIONS: 3 User has Approved/Pending/Declined Withdraw transactions for the past three months (optional)
    PRECONDITIONS: 4 User has Gaming / Casino transactions (optional)
    PRECONDITIONS: 5 User has navigated to the 'My Account' menu
    """
    keep_browser_open = True

    def test_001_navigate_to_history___transactions_history(self):
        """
        DESCRIPTION: Navigate to History -> Transactions History
        EXPECTED: Transactions History page is Opened
        EXPECTED: ![](index.php?/attachments/get/111269055)
        """
        pass

    def test_002_verify_the_transactions_table_after_filter_selection(self):
        """
        DESCRIPTION: Verify the transactions table after filter selection
        EXPECTED: Table can include following transactions:
        EXPECTED: - deposit transactions
        EXPECTED: - gaming / casino transactions
        EXPECTED: etc.
        EXPECTED: ![](index.php?/attachments/get/111269061)
        """
        pass

    def test_003_verify_profitloss__total_stake__total_returns_fields(self):
        """
        DESCRIPTION: Verify Profit/Loss | Total Stake | Total Returns fields
        EXPECTED: Information is shown according to the selected dates and list of transactions
        """
        pass
