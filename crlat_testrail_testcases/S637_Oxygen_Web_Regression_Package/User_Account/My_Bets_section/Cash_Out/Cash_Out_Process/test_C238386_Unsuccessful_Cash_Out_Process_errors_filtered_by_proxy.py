import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C238386_Unsuccessful_Cash_Out_Process_errors_filtered_by_proxy(Common):
    """
    TR_ID: C238386
    NAME: Unsuccessful Cash Out Process (errors filtered by proxy)
    DESCRIPTION: This test case verifies unsuccessful Full and Partial Cash Out Process because of errors filtered by proxy on Cash Out/Open Bets tab
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed in-play/pre match Singles and Multiple bets where Cash Out/Partial cash out offer is available
    PRECONDITIONS: **CORAL**
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: **cashoutStatuses filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED/CASHOUT_LEGSORT_NOT_ALLOWED
    PRECONDITIONS: * CASHOUT_SELN_NO_CASHOUT
    PRECONDITIONS: * DB_ERROR
    PRECONDITIONS: Note: Readbet request/response is sent after successfull partial/full cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successfull partial/full cashout of pre-match events. (Currently works as for in-play events)
    PRECONDITIONS: [How to use Fiddler][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+mock+proxy+responses+using+Fiddler
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab (if available);
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    """
    keep_browser_open = True

    def test_001_navigate_to_cashoutopen_bets_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cashout'/'Open Bets' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: Available events are displayed
        """
        pass

    def test_002_navigate_to_the_single_in_play_bet(self):
        """
        DESCRIPTION: Navigate to the **Single** in-play bet
        EXPECTED: 
        """
        pass

    def test_003_trigger_suberrorcode_cashout_seln_suspended_or_cashout_legsort_not_allowed_for_cashoutbet_response_during_cash_out_attempt_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice_immediately_click_cash_out_and_confrim_cash_out_buttons(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_SELN_SUSPENDED' OR 'CASHOUT_LEGSORT_NOT_ALLOWED' for **cashoutBet** response during cash out attempt:
        DESCRIPTION: * Suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: * Immediately click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        EXPECTED: * Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        EXPECTED: * Timer (Available from OX 99) is NOT displayed
        EXPECTED: * Error message is displayed
        EXPECTED: * User balance is not updated
        """
        pass

    def test_004_verify_error_message(self):
        """
        DESCRIPTION: Verify error message
        EXPECTED: The error message is displayed instead of 'CASH OUT' button with the following information:
        EXPECTED: * Message 'Your Cash Out attempt was unsuccessful, your selection is suspended.' is shown
        EXPECTED: * 'CASH OUT SUSPENDED' greyed out button is shown instead of error message after few seconds. Text is centered.
        """
        pass

    def test_005_verify_error_displaying_logic(self):
        """
        DESCRIPTION: Verify error displaying logic
        EXPECTED: * 'CASH OUT SUSPENDED' button doesn't disappear after scrolling up and down
        EXPECTED: * button text changes back to 'Cash out <value>' ONLY when bet becomes cash out available again
        """
        pass

    def test_006_navigate_to_another_single_pre_match_bet_and_trigger_suberrorcode_cashout_seln_suspended_or_cashout_legsort_not_allowed_click_cash_out_and_confrim_cash_out_buttons_immediately_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice(self):
        """
        DESCRIPTION: Navigate to another Single pre-match bet and trigger subErrorCode 'CASHOUT_SELN_SUSPENDED' OR 'CASHOUT_LEGSORT_NOT_ALLOWED'
        DESCRIPTION: * Click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: * Immediately suspend event or market or selection for event with placed bet in backoffice
        EXPECTED: * Spinner appears on the button instead of the text 'CONFIRM CASH OUT'
        EXPECTED: * Timer (Available from OX 99) is NOT displayed
        EXPECTED: * Error message is displayed
        EXPECTED: * User balance is not updated
        """
        pass

    def test_007_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps #4-5
        EXPECTED: Results are the same
        """
        pass

    def test_008_repeats_steps_3_7_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeats steps #3-7 for **Partial** Cash Out attempt
        EXPECTED: Results are the same
        """
        pass

    def test_009_repeat_steps_3_8_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-8 for **Multiple** bet
        EXPECTED: Results are the same as for the single bet
        """
        pass
