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
class Test_C35443308_Verify_that_the_customer_can_see_the_Bet_History(Common):
    """
    TR_ID: C35443308
    NAME: Verify that the customer can see the Bet History
    DESCRIPTION: Verify that the customer can see the Bet History (Sports, Lotto, Pools)
    DESCRIPTION: Note: cannot automate as we cannot click on date pickers
    PRECONDITIONS: * User should be logged in to view their Bet history
    PRECONDITIONS: * **User should have Bet History for the past three months**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 'Bet history' page is possible to reach:
    PRECONDITIONS: * by clicking/tapping on 'My Bets' tab-> 'Settled Bets' tab at 'Betslip' widget (Desktop/Tablet)
    PRECONDITIONS: * by tapping 'My Bets' button at the Header (Mobile/Tablet)
    PRECONDITIONS: * from the 'My Account' menu -> History -> Betting History
    PRECONDITIONS: * via direct link (e.g., https://sports.coral.co.uk/bet-history) (Desktop/Tablet/Mobile).
    """
    keep_browser_open = True

    def test_001_navigate_to_bet_history_page(self):
        """
        DESCRIPTION: Navigate to 'BET HISTORY' page
        EXPECTED: * 'Bet History' page is opened
        EXPECTED: * "Sports" filter is selected by default
        EXPECTED: * 'To' date picker is set as User's current date
        EXPECTED: * 'From' date picker is set:
        EXPECTED: * as User's 7x days from today's date (For Ladbrokes/Coral from 101.1)
        EXPECTED: * as User's current date (Coral before 101.1)
        EXPECTED: * User's bet history for the 7 Days is displayed (if available)(Ladbrokes/Coral from 101.1)/ for the current date (Coral before 101.1)
        EXPECTED: * Lotto is displayed next to Sports;
        EXPECTED: * Pools is displayed last.
        """
        pass

    def test_002_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_less_than_7_days_past_7_days_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * less than 7 days
        DESCRIPTION: * past 7 days
        DESCRIPTION: * past 1 month
        DESCRIPTION: * past 2 months
        DESCRIPTION: * past 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * User's pending/win/lose/cancelled/cashed out bets for the selected period are displayed
        EXPECTED: * If there are more than 20 events for the selected period, bet details should be loaded after scrolling by portions (20 events by portion)
        """
        pass

    def test_003_verify_the_settled_bets_list(self):
        """
        DESCRIPTION: Verify the 'SETTLED BETS' list
        EXPECTED: The list contains the BET cards that following columns:
        EXPECTED: * Type of Bet
        EXPECTED: * Status of Bet(Won/Lost/Cashed out)
        EXPECTED: * Selection name
        EXPECTED: * Market name
        EXPECTED: * Event name
        EXPECTED: * Stake
        EXPECTED: * Return
        EXPECTED: * Bet Receipt
        EXPECTED: ![](index.php?/attachments/get/14544766)
        """
        pass

    def test_004_verify_data_in_the_list(self):
        """
        DESCRIPTION: Verify data in the list
        EXPECTED: Data in the list corresponds to the data, received in response to
        EXPECTED: **https://ss-aka-ori-dub.coral.co.uk/openbet-ssviewer/Drilldown/2.31/
        EXPECTED: NOTE: For this step, manual calculation of the data, described in previous step, is NOT NEEDED. It's important to verify that we display exactly what we receive.
        """
        pass

    def test_005_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass

    def test_006_select_the_lotto_tab(self):
        """
        DESCRIPTION: Select the Lotto tab
        EXPECTED: * The "Lotto" tab selected
        EXPECTED: * User's  "From" and "To" date pickers remains the same as in the previous Step
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * The list of Lotto bets placed for the current date is displayed (if available)
        """
        pass

    def test_007_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_less_than_7_days_past_7_days_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * less than 7 days
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

    def test_008_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass

    def test_009_select_pools(self):
        """
        DESCRIPTION: Select Pools
        EXPECTED: * The "Pools" tab selected
        EXPECTED: * User's  "From" and "To" date pickers remains the same as in the previous Step
        EXPECTED: * Content of "Settled Bets" accordion is updated according to selected date period
        EXPECTED: * The list of Pools bets placed for the current date is displayed (if available)
        """
        pass

    def test_010_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_less_than_7_days_past_7_days_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * less than 7 days
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

    def test_011_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass
