import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C9608215_Verify_Partial_Cash_Out_History_dropdown(Common):
    """
    TR_ID: C9608215
    NAME: Verify  'Partial Cash Out History' dropdown
    DESCRIPTION: This test case verifies 'Partial Cash Out History' dropdown and its updates
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place SINGLE and MULTIPLE bets with cash out available
    PRECONDITIONS: Should be run on:
    PRECONDITIONS: - Open Bets tab
    PRECONDITIONS: - Bet History tab
    PRECONDITIONS: ![](index.php?/attachments/get/33901)
    PRECONDITIONS: ![](index.php?/attachments/get/33902)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_betsopen_betsbet_historymake_partial_cash_out_for_single_betverify_partial_cash_out_history_dropdown(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets/Bet History
        DESCRIPTION: Make partial cash out for SINGLE bet
        DESCRIPTION: Verify Partial Cash Out History' dropdown
        EXPECTED: - 'Partial cashout successful' message is displayed below the cashout button
        EXPECTED: - 'Partial Cash Out History' dropdown appears with partial cash out data in the table after refresh or navigating back to the page (when success message is not shown)
        """
        pass

    def test_002_make_partial_cash_out_one_more_time_for_single_betverify_that__new_data_is_added_to_partial_cash_out_history_dropdown(self):
        """
        DESCRIPTION: Make Partial cash out one more time for SINGLE bet
        DESCRIPTION: Verify that ' new data is added to 'Partial Cash Out History' dropdown
        EXPECTED: - 'Partial cashout successful' message is displayed below the cashout button
        EXPECTED: - After the message is no longer displayed a new row with partial cashout date is added to 'Partial Cash Out History' table
        """
        pass

    def test_003_make_partial_cash_out_for_multiple_betverify_that_partial_cash_out_history_dropdown_appears(self):
        """
        DESCRIPTION: Make partial cash out for MULTIPLE bet
        DESCRIPTION: Verify that Partial Cash Out History' dropdown appears
        EXPECTED: 'Partial Cash Out History' dropdown appears with partial cash out data in the table (when the success message is no longer displayed - after refresh)
        """
        pass

    def test_004_make_partial_cash_out_one_more_time_for_multiple_betverify_that__new_data_is_added_to_partial_cash_out_history_dropdown(self):
        """
        DESCRIPTION: Make Partial cash out one more time for MULTIPLE bet
        DESCRIPTION: Verify that ' new data is added to 'Partial Cash Out History' dropdown
        EXPECTED: A new row with partial cash out date is added to 'Partial Cash Out History' table (when the success message is no longer displayed - after refresh)
        """
        pass
