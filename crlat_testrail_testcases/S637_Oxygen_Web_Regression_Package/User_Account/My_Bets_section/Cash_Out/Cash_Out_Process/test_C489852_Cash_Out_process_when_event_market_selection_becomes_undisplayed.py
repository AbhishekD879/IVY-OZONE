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
class Test_C489852_Cash_Out_process_when_event_market_selection_becomes_undisplayed(Common):
    """
    TR_ID: C489852
    NAME: Cash Out process when event/market/selection becomes undisplayed
    DESCRIPTION: This test case verifies Cash Out process when event/market/selection becomes undisplayed
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: AUTOTEST [C9698081] [C1700189]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successfull partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successfull partial cashout of of pre-match events. (Currently works as for in-play events)
    PRECONDITIONS: **Currently CASH OUT option is available on back-end for Football, Tennis, Darts and Snooker (other sports will be added in future).**
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_page__tab_on_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' page / tab on 'Bet Slip' widget
        EXPECTED: 'Cash Out' page / tab is opened
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
        EXPECTED: Spinner with count down timer in format XX:XX appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_006_wait_until_button_with_spinner_with_count_down_timer_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner with count down timer disappears
        EXPECTED: * 'Cashed out' label is displayed ath the top right corner on the header
        EXPECTED: * Green "tick" in a circle and message "You cashed out <currency> <value>" is shown below the header
        EXPECTED: * Message "Cashout Successfully" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        """
        pass

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on cashed out value
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
