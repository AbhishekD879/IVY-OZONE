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
class Test_C324773_Unsuccessful_Cash_Out_Process_errors_NOT_filtered_by_proxy(Common):
    """
    TR_ID: C324773
    NAME: Unsuccessful Cash Out Process (errors NOT filtered by proxy)
    DESCRIPTION: This test case verifies unsuccessful Full and Partial Cash Out Process because of errors NOT filtered by proxy on Cash Out tab
    DESCRIPTION: **TO EDIT:** There is incorrect information about triggering some statuses, described in the steps.
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial/full cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial/full cashout of pre-match events. (Currently, works as for in-play events)
    PRECONDITIONS: [How to use Fiddler][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+mock+proxy+responses+using+Fiddler
    PRECONDITIONS: [How to trigger specific 'subErrorCodes'][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/pages/viewpage.action?pageId=58391155
    PRECONDITIONS: **From release XXX.XX:**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    PRECONDITIONS: - initial bets data will be returned after establishing connection
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_single_bet(self):
        """
        DESCRIPTION: Navigate to the **Single** bet
        EXPECTED: 
        """
        pass

    def test_003_trigger_suberrorcode_cashout_seln_suspended_for_cashoutbet_response_during_cash_out_attempt_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice_immediately_click_cash_out_and_confrim_cash_out_buttonsor_using_fiddler_tool_mock_response_in_cashoutbet_responseor(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_SELN_SUSPENDED' for **cashoutBet** response during cash out attempt:
        DESCRIPTION: * Suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: * Immediately click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: OR
        DESCRIPTION: * Using **Fiddler tool mock** response in cashoutBet response
        DESCRIPTION: OR
        EXPECTED: * Error message is displayed
        EXPECTED: * User balance is not updated
        EXPECTED: *The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Message is displayed with the text **'Your Cash Out attempt was unsuccessful, your selection is suspended.'**
        """
        pass

    def test_004_trigger_suberrorcode_cashout_cust_restrict_flag_for_cashoutbet_response_during_cash_out_attempt_using_instruction_from_precondition_to_trigger_cashout_cust_restrict_flag(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_CUST_RESTRICT_FLAG' for **cashoutBet** response during cash out attempt:
        DESCRIPTION: * Using instruction from Precondition to trigger 'CASHOUT_CUST_RESTRICT_FLAG'
        EXPECTED: * Error message is displayed
        EXPECTED: * User balance is not updated
        EXPECTED: * The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Message is displayed with the text **'Sorry, we cannot authorise Cash Out from your account. Please contact us if you feel this may be an error.'**
        """
        pass

    def test_005_verify_errors_displaying_logic(self):
        """
        DESCRIPTION: Verify errors displaying logic
        EXPECTED: * Errors don't disappear after scrolling up and down or collapsing-expanding bet accordion
        EXPECTED: * After 5 seconds **bet with error is removed** from the Cash Out section
        EXPECTED: * After page refresh bet is not displayed on the Cash Out section
        """
        pass

    def test_006_navigate_to_another_single_bet_and_trigger_suberrorcode_cashout_seln_suspended_or_cashout_cust_restrict_flag_for_readbet_response_during_cash_out_attempt_click_cash_out_and_confrim_cash_out_buttons_immediately_suspend_event_or_market_or_selection_for_event_with_placed_bet_in_backoffice_using_fiddler_tool_mock_response_in_readbet_response_using_instruction_from_precondition_to_trigger_cashout_cust_restrict_flag(self):
        """
        DESCRIPTION: Navigate to another Single bet and trigger subErrorCode 'CASHOUT_SELN_SUSPENDED' OR 'CASHOUT_CUST_RESTRICT_FLAG' for **readBet** response during cash out attempt:
        DESCRIPTION: * Click 'CASH OUT' and 'CONFRIM CASH OUT' buttons
        DESCRIPTION: * Immediately suspend event or market or selection for event with placed bet in backoffice
        DESCRIPTION: * Using **Fiddler tool mock** response in readBet response
        DESCRIPTION: * Using instruction from Precondition to trigger 'CASHOUT_CUST_RESTRICT_FLAG'
        EXPECTED: Results are the same as in steps 3-5
        """
        pass

    def test_007_repeats_steps_3_6_for_partial_cash_out_attempt(self):
        """
        DESCRIPTION: Repeats steps #3-6 for **Partial** Cash Out attempt
        EXPECTED: Results are the same
        """
        pass

    def test_008_repeat_steps_3_6_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-6 for **Multiple** bet
        EXPECTED: Results are the same
        """
        pass

    def test_009_trigger_suberrorcode_cashout_bet_cashed_out(self):
        """
        DESCRIPTION: Trigger subErrorCode 'CASHOUT_BET_CASHED_OUT'
        EXPECTED: * Error message is displayed
        EXPECTED: * User balance is not updated
        EXPECTED: *The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Message is displayed with the text **'Your Cash Out attempt was unsuccessful, as your bet has already been Cashed Out.'**
        """
        pass

    def test_010_trigger_for_suberrorcode_cashout_bet_settled(self):
        """
        DESCRIPTION: Trigger for subErrorCode 'CASHOUT_BET_SETTLED'
        EXPECTED: * Error message is displayed
        EXPECTED: * User balance is not updated
        EXPECTED: *The error message is displayed instead of 'CASH OUT' button and slider with the following information:
        EXPECTED: * Message is displayed with the text **'Your Cash Out attempt was unsuccessful, as your bet has already been settled.'**
        """
        pass

    def test_011_repeat_steps_2_9_for_any_other_suberrorcode_not_filtered_by_proxy_for_example_cashout_unavailable__sys_no_cashout_using_fiddler_tool(self):
        """
        DESCRIPTION: Repeat steps #2-9 for any other subErrorCode not filtered by proxy (for example 'CASHOUT_UNAVAILABLE_ SYS_NO_CASHOUT' (using Fiddler tool))
        EXPECTED: Results are the same except in step #4:
        EXPECTED: * Underneath previous box second message is not shown
        """
        pass

    def test_012_repeat_steps_2_9_for_absence_of_suberrorcode__using_fiddler_tool(self):
        """
        DESCRIPTION: Repeat steps #2-9 for absence of subErrorCode  (using Fiddler tool)
        EXPECTED: Results are the same except in step #4:
        EXPECTED: * Underneath previous box second message is not shown
        """
        pass
