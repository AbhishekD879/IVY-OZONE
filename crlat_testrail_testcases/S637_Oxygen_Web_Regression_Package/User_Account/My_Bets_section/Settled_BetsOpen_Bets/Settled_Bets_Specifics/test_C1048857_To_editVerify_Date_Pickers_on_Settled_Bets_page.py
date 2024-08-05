import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1048857_To_editVerify_Date_Pickers_on_Settled_Bets_page(Common):
    """
    TR_ID: C1048857
    NAME: [To-edit]Verify Date Pickers on Settled Bets page
    DESCRIPTION: [T0-Edit] - needs to be edited according to all changes with Vanilla
    DESCRIPTION: This test case verifies date pickers on 'Settled Bets' tab on 'My Bets' and on 'Account History' pages
    PRECONDITIONS: 1. User should be logged in to see his Settled Betsy.
    PRECONDITIONS: 2. User should have a few open/won/settled/void/cashed out bets
    PRECONDITIONS: 3. User should have bets that were reviewed by Overask functionality (rejected, offered and so on)
    """
    keep_browser_open = True

    def test_001_open_settled_bets_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Open 'Settled Bets' tab on 'My Bets' page
        EXPECTED: * 'Settled Bets' tab on 'My Bets' page is opened
        EXPECTED: * "Regular" filter is selected by default
        EXPECTED: * "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        EXPECTED: * User's bet history for the current date is displayed (if available)
        """
        pass

    def test_002_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_past_1_day_past_1_month_past_2_months_past_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of:
        DESCRIPTION: * past 1 day
        DESCRIPTION: * past 1 month
        DESCRIPTION: * past 2 months
        DESCRIPTION: * past 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's pending/win/lose/cancelled/cashed out bets for the selected period are displayed
        EXPECTED: * If there are more than 20 events for the selected period,  bet details should be loaded after scrolling by portions (20 events by portion)
        """
        pass

    def test_003_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: Date pickers are sticky and remain below the sticky page header while user is scrolling
        EXPECTED: NOTE: Sticky date pickers are not yet implemented.
        """
        pass

    def test_004_scroll_down_the_page_and_change_dates_in_the_pickers(self):
        """
        DESCRIPTION: Scroll down the page and change dates in the pickers
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is displayed
        EXPECTED: NOTE: Sticky date pickers are not yet implemented.
        """
        pass

    def test_005_select_dates_in_start_and_end_date_pickers_in_order_to_create_a_date_range_of_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in "Start" and "End" date pickers in order to create a date range of more than last 3 months
        EXPECTED: * Dates are set in the pickers
        EXPECTED: * Date range filter is applied
        EXPECTED: * User's bet history for the selected period is NOT displayed
        EXPECTED: * Message is displayed: **"If you require account or gambling history over longer periods please contact us**
        """
        pass

    def test_006_tap_contact_us_link(self):
        """
        DESCRIPTION: Tap 'contact us' link
        EXPECTED: User is redirected (in new tab) to the 'contact us' page (https://help.coral.co.uk/s/article/Contact-Us)
        """
        pass

    def test_007_select_todays_date_in_the_start_date_picker_and_some_future_date_in_the_end_date_picker(self):
        """
        DESCRIPTION: Select today's date in the "Start" date picker and some future date in the "End" date picker
        EXPECTED: * User's history for the current date is shown (if available)
        EXPECTED: * ***"You have no bet history"*** message is shown if user has no bet history for the current date
        """
        pass

    def test_008_select_a_future_date_in_the_start_date_picker_and_a_past_date_in_the_end_date_picker(self):
        """
        DESCRIPTION: Select a **future** date in the "Start" date picker and a **past** date in the "End" date picker
        EXPECTED: * ***"Please select a valid time range"*** error message is shown
        """
        pass

    def test_009_repeat_steps_2_8_with_lotto_filter_selected(self):
        """
        DESCRIPTION: Repeat steps 2-8 with "Lotto" filter selected
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_8_with_pools_filter_selected(self):
        """
        DESCRIPTION: Repeat steps 2-8 with "Pools" filter selected
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_1_10_for_settled_bets_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop_settled_bets_page_for_tabletdesktop___can_be_reached_via_direct_link_eg_httpsinvictuscoralcoukbet_history(self):
        """
        DESCRIPTION: Repeat steps 1-10 for:
        DESCRIPTION: * Settled Bets tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        DESCRIPTION: * "Settled Bets" page (for Tablet/Desktop) - can be reached via direct link (e.g., https://invictus.coral.co.uk/#/bet-history)
        EXPECTED: 
        """
        pass
