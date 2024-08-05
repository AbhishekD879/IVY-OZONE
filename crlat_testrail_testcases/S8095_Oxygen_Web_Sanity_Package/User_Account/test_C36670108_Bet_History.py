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
class Test_C36670108_Bet_History(Common):
    """
    TR_ID: C36670108
    NAME: Bet History
    DESCRIPTION: Verify that the customer can see the Bet History (Sports, Lotto, Pools, Player Bets)
    PRECONDITIONS: * User should be logged in to view their Bet history
    PRECONDITIONS: * **User should have Bet History for the past three months**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 'Bet history' page is possible to reach by clicking on 'My Bets'-> 'Settled Bets' tab at 'Betslip' widget (Desktop/Tablet) and 'My Bets' button at the Header (Mobile/Tablet), from the 'My Account' menu (Desktop/Tablet/Mobile) and via direct link (e.g., https://invictus.coral.co.uk/#/bet-history) (Desktop/Tablet/Mobile).
    PRECONDITIONS: **Note 2:**
    PRECONDITIONS: 'Profit/Loss' is now a link to mobileportal/transactions page (was changed from Vanilla side)
    """
    keep_browser_open = True

    def test_001_navigate_to_bet_history_page(self):
        """
        DESCRIPTION: Navigate to 'BET HISTORY' page
        EXPECTED: * 'Bet History' page is opened
        EXPECTED: * "Sports" filter is selected by default
        EXPECTED: * "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: * "PROFIT/LOSS" accordion (collapsed by default)
        EXPECTED: * User's bet history for the current date is displayed (if available)
        EXPECTED: * 'Lotto' is displayed next to 'Sports'
        EXPECTED: * 'Pools' is displayed last.
        """
        pass

    def test_002_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * past 1 month
        DESCRIPTION: * past 2 months
        DESCRIPTION: * past 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * User's pending/win/lose/cancelled/cashed out bets for the selected period are displayed (all collapsed by default)
        EXPECTED: * If there are more than 20 events for the selected period, bet details should be loaded after scrolling by portions (20 events by portion)
        """
        pass

    def test_003_expand_the_profitloss_accordion(self):
        """
        DESCRIPTION: Expand the "PROFIT/LOSS" accordion
        EXPECTED: * Accordion is expanded
        EXPECTED: * Table is shown
        """
        pass

    def test_004_verify_the_profitloss_table(self):
        """
        DESCRIPTION: Verify the "PROFIT/LOSS" table
        EXPECTED: The table contains the following columns:
        EXPECTED: * **Sports** - total profit/loss for the user
        EXPECTED: * **T. STAKES** - showing the total stakes for the user
        EXPECTED: * **T. RETURNS** - showing the total returns for the user
        """
        pass

    def test_005_verify_data_in_the_table(self):
        """
        DESCRIPTION: Verify data in the table
        EXPECTED: Data in the table corresponds to the data, received in response to **wss://openapi.egalacoral.com/socket.io/1/websocket/** {"ID":32012,"} request to Playtech.
        EXPECTED: NOTE: For this step, manual calculation of the data, described in the previous step, is NOT NEEDED. It's important to verify that we display exactly what we receive from Playtech.
        """
        pass

    def test_006_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass

    def test_007_select_the_lotto_tab(self):
        """
        DESCRIPTION: Select the Lotto tab
        EXPECTED: * The "Lotto" tab selected
        EXPECTED: * User's  "From" and "To" date pickers remains the same as in Step 6
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * The list of Lotto bets placed for the current date is displayed (if available)
        """
        pass

    def test_008_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_past_7_days_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * past 7 days
        DESCRIPTION: * past 1 month
        DESCRIPTION: * past 2 months
        DESCRIPTION: * past 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * Lotto Bets placed for the selected period are displayed
        """
        pass

    def test_009_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass

    def test_010_select_pools(self):
        """
        DESCRIPTION: Select Pools
        EXPECTED: * The "Pools" tab selected
        EXPECTED: * User's  "From" and "To" date pickers remains the same as in Step 9
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * The list of Pools bets placed for the current date is displayed (if available)
        """
        pass

    def test_011_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_past_7_days_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * past 7 days
        DESCRIPTION: * past 1 month
        DESCRIPTION: * past 2 months
        DESCRIPTION: * past 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * Pool Bets placed for the selected period are displayed
        """
        pass

    def test_012_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass
