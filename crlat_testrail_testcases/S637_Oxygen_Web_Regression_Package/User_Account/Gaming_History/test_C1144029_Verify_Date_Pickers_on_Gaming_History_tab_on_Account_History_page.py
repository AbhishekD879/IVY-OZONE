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
class Test_C1144029_Verify_Date_Pickers_on_Gaming_History_tab_on_Account_History_page(Common):
    """
    TR_ID: C1144029
    NAME: Verify Date Pickers on 'Gaming History' tab on 'Account History' page
    DESCRIPTION: This test case verifies date pickers on 'Gaming History' tab on 'Account History' page
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: * [BMA-23956 RTS: Account History > Gaming History] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-23956
    PRECONDITIONS: * User should be logged in to view their Gaming history
    PRECONDITIONS: * User should have Gaming History
    """
    keep_browser_open = True

    def test_001_go_to_my_account___gaming_history(self):
        """
        DESCRIPTION: Go to 'My Account' -> 'Gaming History'
        EXPECTED: * 'Gaming History' tab on 'Account History' page is opened
        EXPECTED: * "From" and "To" date pickers with user's current date selected by default in both of them
        EXPECTED: * 'gaming history' table is shown with data from today's date
        """
        pass

    def test_002_verify_data_displaying_in_gaming_history_table(self):
        """
        DESCRIPTION: Verify data displaying in 'gaming history' table
        EXPECTED: The data is organised and displayed in a table into following columns:
        EXPECTED: *   **'Date/Time'** column is shown in** DD-MM HH:MM AM/PM** format (e.g 04/05 06:45 AM)
        EXPECTED: *   **'Game'** column is shown in **\[client type] wager: [game\_name\] ([game\_category]) **format (e.g. Casino wager: Blackjack Multihand 5 (Cards))
        EXPECTED: *   **'Amount' **coulmn is shown in** **+-**\[currencyCode\]\[amount\] **format (e.g. £+10.00)
        """
        pass

    def test_003_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_past_7_days_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * past 7 days
        DESCRIPTION: * past 1 month
        DESCRIPTION: * past 2 months
        DESCRIPTION: * past 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Table with gaming history for the selected period is displayed
        """
        pass

    def test_004_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: (not yet implemented) Date pickers are sticky and remain below the sticky page header while user is scrolling
        """
        pass

    def test_005_scroll_down_the_page_and_change_dates_in_the_pickers(self):
        """
        DESCRIPTION: Scroll down the page and change dates in the pickers
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Table with gaming history for the selected period is displayed
        """
        pass

    def test_006_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * Table with gaming history for the selected period is *NOT* displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us"**
        """
        pass

    def test_007_tap_contact_us_link(self):
        """
        DESCRIPTION: Tap 'contact us' link
        EXPECTED: User is redirected (in new tab) to the 'contact us' page ( https://help.coral.co.uk/s/article/Contact-Us)
        """
        pass

    def test_008_select_todays_date_in_the_start_date_picker_and_some_future_date_in_the_end_date_picker(self):
        """
        DESCRIPTION: Select today's date in the "Start" date picker and some future date in the "End" date picker
        EXPECTED: * Table with gaming history for the current date is shown (if available)
        EXPECTED: * ***"You have no gaming history"*** message is shown if user has no gaming history for the current date
        """
        pass

    def test_009_select_a_future_date_in_the_start_date_picker_and_a_past_date_in_the_end_date_picker(self):
        """
        DESCRIPTION: Select a **future** date in the "Start" date picker and a **past** date in the "End" date picker
        EXPECTED: * ***"Please select a valid time range"*** error message is shown
        """
        pass
