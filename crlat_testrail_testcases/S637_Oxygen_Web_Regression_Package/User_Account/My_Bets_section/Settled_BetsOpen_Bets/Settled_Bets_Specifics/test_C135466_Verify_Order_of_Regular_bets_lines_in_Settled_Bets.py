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
class Test_C135466_Verify_Order_of_Regular_bets_lines_in_Settled_Bets(Common):
    """
    TR_ID: C135466
    NAME: Verify Order of Regular bets lines in Settled Bets
    DESCRIPTION: This test case verifies order of 'Regular' bet lines on 'Settled Bets' tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Place simultaneously a few bets (multiples and singles) (in order to get the same Bet Placement Time) including YourCall bets
    PRECONDITIONS: * Place a few bets (multiples and singles) at different time (in order to get bet lines with different Bet Placement Time)
    PRECONDITIONS: * Place simultaneously a few bets on the same event but different markets/selections (in order to get the same Bet Placement Time and Event Start Time)
    PRECONDITIONS: NOTE: All placed bets should be already **settled**
    PRECONDITIONS: Note:
    PRECONDITIONS: Bets from YourCall Markets are displayed within Regular bets Tab
    """
    keep_browser_open = True

    def test_001_navigate_to_settled_bets_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' tab is opened
        EXPECTED: * 'Regular' sort filter is selected by default
        EXPECTED: * "From" and "To" date pickers with user's current date selected by default in 'To' date picker and 7x days from today's date in 'From' date packer
        EXPECTED: (Example:
        EXPECTED: User logged in today 23/10: Default dates should be 17/10 to 23/10 (today's date +6 days totalling 7 days))
        """
        pass

    def test_002_verify_order_of_bets_within_the_same_date_panel(self):
        """
        DESCRIPTION: Verify order of bets within the same date panel
        EXPECTED: All bets are ordered chronologically by bet placement time (the most recent first)
        """
        pass

    def test_003_verify_order_of_bets_with_the_same_bet_placement_time(self):
        """
        DESCRIPTION: Verify order of bets with the same bet placement time
        EXPECTED: *   Bet lines are ordered by Event Start Time (with the earliest start time first)
        EXPECTED: *   In case of the same Event Start Time - in the order they come back from betplacement API (accountHistory response)
        """
        pass

    def test_004_select_dates_in_the_from_and_to_date_pickers_but_no_more_than_last_3_months(self):
        """
        DESCRIPTION: Select dates in the "From" and "To" date pickers (but no more than last 3 months)
        EXPECTED: Dates are selected and the time range filter is applied
        """
        pass

    def test_005_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_006_select_some_different_dates_in_order_to_change_time_range_eg_last_3_days_1_month_and_repeat_steps_3_4(self):
        """
        DESCRIPTION: Select some different dates in order to change time range (e.g., last 3 days, 1 month...) and repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_7_for_bet_history_tab_account_history_page_for_mobile_bet_slip_widget_for_tabletdesktop(self):
        """
        DESCRIPTION: Repeat steps 2-7 for:
        DESCRIPTION: * Bet History tab 'Account History' page (for mobile)
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        EXPECTED: 
        """
        pass
