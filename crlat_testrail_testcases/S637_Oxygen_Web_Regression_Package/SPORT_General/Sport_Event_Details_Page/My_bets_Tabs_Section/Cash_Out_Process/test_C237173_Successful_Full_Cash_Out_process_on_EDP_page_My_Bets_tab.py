import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C237173_Successful_Full_Cash_Out_process_on_EDP_page_My_Bets_tab(Common):
    """
    TR_ID: C237173
    NAME: Successful Full Cash Out process on EDP page > My Bets tab
    DESCRIPTION: This test case verifies successful Full Cash Out process on 'My Bets' tab on Event Details page
    DESCRIPTION: AUTOTEST [C2012650] (in scope of Test_C237173_C237766_Successful_Full_and_Partial_Cash_Out_process)
    DESCRIPTION: **Coral Only**
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful full cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful full cashout of pre-match events. (Currently works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed Single bet with available cash out
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_002_tap_cash_out_button_eg_cash_out_valueremains_unchanged(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button (e.g. cash out value remains unchanged)
        EXPECTED: 
        """
        pass

    def test_003_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_004_wait_untilbutton_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: * 'Cashed out' label is displayed at the top right corner on the header
        EXPECTED: * Green "tick" in a circle and message "You cashed out <currency> <value>" is shown below the header
        EXPECTED: * Message "Cashout Successfully" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        """
        pass

    def test_005_verify_the_bet_presence_on_the_tab(self):
        """
        DESCRIPTION: Verify the bet presence on the tab
        EXPECTED: The bet is NOT removed from the 'My Bets' tab automatically
        """
        pass

    def test_006_navigate_to_any_other_page_and_then_go_back_to_your_event_edp_page__my_bets_tab_or_just_refresh_the_edp_page__my_bets_tab_page(self):
        """
        DESCRIPTION: Navigate to any other page and then go back to your event EDP page > My Bets tab or just refresh the EDP page > My Bets tab page
        EXPECTED: Previously cashed out bet is not present on EDP page > My Bets tab
        EXPECTED: **Note:** if there was only one bet on 'My Bets' tab then after successful Full Cash Out and page refresh 'My Bets' tab disappears
        """
        pass

    def test_007_verify_other_bet_lines_after_removing_fully_cashed_out_bet(self):
        """
        DESCRIPTION: Verify other bet lines after removing fully cashed out bet
        EXPECTED: **All** bet lines are updated
        """
        pass

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on full cash out value
        """
        pass

    def test_009_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed Multiple bets with available cash out
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_8_for_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Repeat steps №2-8 for **Multiple** Cash Out bet lines
        EXPECTED: 
        """
        pass
