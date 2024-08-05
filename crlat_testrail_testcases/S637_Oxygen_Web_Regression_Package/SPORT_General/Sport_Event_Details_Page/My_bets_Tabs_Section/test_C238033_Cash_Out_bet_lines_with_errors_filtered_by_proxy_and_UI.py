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
class Test_C238033_Cash_Out_bet_lines_with_errors_filtered_by_proxy_and_UI(Common):
    """
    TR_ID: C238033
    NAME: Cash Out bet lines with errors filtered by proxy and UI
    DESCRIPTION: This test case verifies displaying of error messages filtered by proxy during loading and sitting on 'My Bets' tab on Event Details page
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Single and Multiple bets with available cash out
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **cashoutStatuses filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED(need to suspend event/market/selection)
    PRECONDITIONS: * CASHOUT_SELN_NO_CASHOUT ( need to disable cashout for event/market)
    PRECONDITIONS: * DB_ERROR ( mock in Fiddler tool)
    PRECONDITIONS: **NOTE**
    PRECONDITIONS: errors received in **getbetDetails** in filtered by proxy
    PRECONDITIONS: errors received in **getbetDetail** in filtered by UI part
    PRECONDITIONS: From version XXX.XX **getbetDetail** should be removed.
    PRECONDITIONS: For now there is no known way how to trigger cashoutStatus DB_ERROR in OB Backoffice. Fiddler tool can be used to mock responses.
    PRECONDITIONS: How to use Fiddler tool: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+mock+proxy+responses+using+Fiddler
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_first_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of first event with placed **Single** bet with available cash out
        EXPECTED: * 'My Bets' tab is opened
        EXPECTED: * Bet is shown without error message
        """
        pass

    def test_002_in_ob_backoffice_trigger_suberrorcode_cashout_seln_suspended_in_getbetdetail_response_for_single_cash_out_betfrom_version_xxxxx_getbetdetail_should_be_removedsuspend_event_or_market_or_selection_for_event_with_placed_bet(self):
        """
        DESCRIPTION: In OB Backoffice trigger subErrorCode: "CASHOUT_SELN_SUSPENDED" in **getbetDetail** response for **Single** Cash Out bet
        DESCRIPTION: (From version XXX.XX **getbetDetail** should be removed)
        DESCRIPTION: (Suspend event or market or selection for event with placed bet)
        EXPECTED: Greyed 'CASH OUT SUSPENDED' button appears instead of 'CASH OUT' and 'Partial CashOut' buttons.
        EXPECTED: Text of message is centered.
        """
        pass

    def test_003_tap_somewhere_else_not_by_message_or_scroll_updown_and_remove_finger(self):
        """
        DESCRIPTION: Tap somewhere else (not by message) or scroll up/down and remove finger
        EXPECTED: Greyed 'CASH OUT SUSPENDED' button does not disappear
        """
        pass

    def test_004_navigate_to_another_page_and_return_back_to_my_bets_tab_on_event_details_page_of_suspended_event(self):
        """
        DESCRIPTION: Navigate to another page and return back to 'My bets' tab on Event Details page of suspended event
        EXPECTED: * Single bet is shown with the same Greyed 'CASH OUT SUSPENDED' button as in step #2
        EXPECTED: * cashoutStatus: "CASHOUT_SELN_SUSPENDED" OR "CASHOUT_LEGSORT_NOT_ALLOWED" is received in **getbetDetails** response
        EXPECTED: **From release XXX.XX:**
        EXPECTED: * WS connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
        EXPECTED: * initial bets data will be returned after establishing connection (cashoutValue: "CASHOUT_SELN_SUSPENDED" for an appropriate bet)
        """
        pass

    def test_005_in_ob_backoffice_unsuspend_event(self):
        """
        DESCRIPTION: In OB Backoffice unsuspend event
        EXPECTED: 'CASH OUT' and 'Partial CashOut' buttons are shown under bet details instead of Greyed 'CASH OUT SUSPENDED' button
        """
        pass

    def test_006_navigate_to_my_bets_tab_on_event_details_page_of_second_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of second event with placed **Single** bet with available cash out
        EXPECTED: * 'My Bets' tab is opened
        EXPECTED: * Bet is shown without error message and Greyed 'CASH OUT SUSPENDED' button
        """
        pass

    def test_007_click_cashout_button_confirm_cashout_and_simultaneously_trigger_cashoutvalue_cashout_seln_no_cashout_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_toolfrom_version_xxxxx_getbetdetail_should_be_removeduntick_cashout_parametr_on_event_level_in_ti(self):
        """
        DESCRIPTION: Click 'Cashout' button, confirm cashout and simultaneously trigger cashoutValue: "CASHOUT_SELN_NO_CASHOUT" in **getbetDetail** response for **Single** Cash Out bet (e.g. mock response with Fiddler tool)
        DESCRIPTION: (From version XXX.XX **getbetDetail** should be removed)
        DESCRIPTION: (Untick Cashout parametr on Event level in TI)
        EXPECTED: *   Error message of **One or more events in your bet are not available for Cash Out.** is shown below bet line details instead of 'CASH OUT' button. Text of message is centered.
        """
        pass

    def test_008_verify_errors_displaying_logic(self):
        """
        DESCRIPTION: Verify errors displaying logic
        EXPECTED: * Errors don't disappear after scrolling up and down or collapsing-expanding bet accordion
        EXPECTED: * After 5 seconds **bet with error is removed** from the Cash Out section
        EXPECTED: * After page refresh bet is not displayed on the Cash Out section
        """
        pass

    def test_009_go_to_third_verified_single_cash_out_bet_line_and_move_partial_cashout_slider_to_any_value_not_to_100(self):
        """
        DESCRIPTION: Go to third verified Single Cash Out bet line and move Partial CashOut slider to any value (not to 100%)
        EXPECTED: 
        """
        pass

    def test_010_click_cashout_button_confirm_cashout_and_simultaneously_trigger_cashoutstatus_db_error_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_toolfrom_version_xxxxx_getbetdetail_should_be_removed(self):
        """
        DESCRIPTION: Click 'Cashout' button, confirm cashout and simultaneously trigger cashoutStatus: "DB_ERROR" in getbetDetail response for **Single** Cash Out bet (e.g. mock response with Fiddler tool)
        DESCRIPTION: (From version XXX.XX **getbetDetail** should be removed.)
        EXPECTED: *   Error message of **CASH OUT UNSUCCESSFUL, PLEASE TRY AGAIN** is shown below bet line details instead of 'CASH OUT' and 'Partial CashOut' buttons. Text of message is centered.
        """
        pass

    def test_011_go_to_first_multiples_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to first **Multiples** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_012_in_ob_backoffice_trigger_suberrorcode_cashout_seln_suspended__in_getbetdetail_response_for_multiple_cash_out_betfrom_version_xxxxx_getbetdetail_should_be_removedsuspend_event_or_market_or_selection_for_event_with_placed_bet(self):
        """
        DESCRIPTION: In OB Backoffice trigger subErrorCode: "CASHOUT_SELN_SUSPENDED"  in **getbetDetail** response for **Multiple** Cash Out bet
        DESCRIPTION: (From version XXX.XX **getbetDetail** should be removed)
        DESCRIPTION: (Suspend event or market or selection for event with placed bet)
        EXPECTED: Greyed 'CASH OUT SUSPENDED' button appears instead of 'CASH OUT' and 'Partial CashOut' buttons.
        EXPECTED: Text of message is centered.
        """
        pass

    def test_013_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_7_10_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #7-10 for Multiple bets
        EXPECTED: 
        """
        pass

    def test_015_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Bets are shown with relevant error messages (if cashoutStatus filtered by proxy is received in **getbetdetails** response)
        EXPECTED: (From version XXX.XX **getbetDetail** should be removed.)
        EXPECTED: *   Error message of **CASH OUT UNSUCCESSFUL, PLEASE TRY AGAIN** is shown below bet line details instead of 'CASH OUT' and 'Partial CashOut' buttons. Text of message is centered.
        """
        pass
