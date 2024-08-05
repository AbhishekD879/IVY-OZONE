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
class Test_C511991_Cash_Out_process_when_event_market_selection_becomes_undisplayed(Common):
    """
    TR_ID: C511991
    NAME: Cash Out process when event/market/selection becomes undisplayed
    DESCRIPTION: This test case verifies Cash Out process when event/market/selection becomes undisplayed on 'My Bets' tab on Event Details page
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of pre-match events. (Currently, works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: * WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: * initial bets data will be returned after establishing connection
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cashout(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cashout
        EXPECTED: 
        """
        pass

    def test_002_go_to_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_tap_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        EXPECTED: 
        """
        pass

    def test_004_trigger_undisplaying_in_openbet_ti_tool_for_current_eventmarketselection(self):
        """
        DESCRIPTION: Trigger undisplaying in Openbet TI tool for current event/market/selection
        EXPECTED: Event/market/selection becomes undisplayed
        """
        pass

    def test_005_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_006_wait_until_button_with_spinner_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner disappears
        EXPECTED: The success message is displayed instead of 'CASH OUT' button with the following information:
        EXPECTED: *   Green box with "tick" in a circle and message of "SUCCESSFUL CASH OUT" are shown below bet line details. The icon and text are centered within green box.
        """
        pass

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: 
        """
        pass

    def test_008_navigate_to_multiple_cash_out_bet_line_and_repeat_steps_1_7(self):
        """
        DESCRIPTION: Navigate to **Multiple** Cash Out bet line and repeat steps #1-7
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_8_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeat steps #1-8 for **Partial Cash Out** attempt
        EXPECTED: 
        """
        pass
