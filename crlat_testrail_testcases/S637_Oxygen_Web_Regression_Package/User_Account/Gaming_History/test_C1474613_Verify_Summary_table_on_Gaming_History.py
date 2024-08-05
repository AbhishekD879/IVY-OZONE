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
class Test_C1474613_Verify_Summary_table_on_Gaming_History(Common):
    """
    TR_ID: C1474613
    NAME: Verify "Summary" table on Gaming History
    DESCRIPTION: This test case verifies "Summary" table on 'Gaming History' page
    PRECONDITIONS: 1. User should be logged in to see his Gaming History.
    PRECONDITIONS: 2. User should have gaming history available
    """
    keep_browser_open = True

    def test_001_go_to_my_account___gaming_history(self):
        """
        DESCRIPTION: Go to "My Account" -> "Gaming History"
        EXPECTED: * 'Gaming History' page is opened
        EXPECTED: * User's current date is selected in both "From" and "To" date pickers
        EXPECTED: * User's gaming history for the current date is displayed (if available)
        """
        pass

    def test_002_set_a_date_range_in_the_date_pickers_in_order_to_see_users_gaming_history(self):
        """
        DESCRIPTION: Set a date range in the date pickers in order to see user's Gaming History
        EXPECTED: Gaming History for the selected time period appears
        """
        pass

    def test_003_verify_summary_table_under_the_date_pickers(self):
        """
        DESCRIPTION: Verify 'Summary' table under the date pickers
        EXPECTED: The table contains the following columns:
        EXPECTED: * **T. Stakes** - showing the total stakes for the user
        EXPECTED: * **T. Returns** - showing the total returns for the user
        EXPECTED: * **Profit/Loss** - total profit/loss for the user
        """
        pass

    def test_004_verify_data_in_the_table(self):
        """
        DESCRIPTION: Verify data in the table
        EXPECTED: Data in the table corresponds to the data, received in response to wss://openapi.egalacoral.com/socket.io/1/websocket/ {"ID":32012,"} request to Playtech.
        EXPECTED: NOTE: For this step, manual calculation of the data, described in previous step, is NOT NEEDED. It's important to verify that we display exactly what we receive from Playtech.
        """
        pass

    def test_005_repeat_steps_1_4_for_users_with_the_following_currencies_gbp_eur_usd_sek(self):
        """
        DESCRIPTION: Repeat steps 1-4 for users with the following currencies:
        DESCRIPTION: * GBP
        DESCRIPTION: * EUR
        DESCRIPTION: * USD
        DESCRIPTION: * SEK
        EXPECTED: * Correct data is displayed in the table for every user with different currency
        EXPECTED: * Corresponding currency symbol is displayed in the table
        """
        pass
