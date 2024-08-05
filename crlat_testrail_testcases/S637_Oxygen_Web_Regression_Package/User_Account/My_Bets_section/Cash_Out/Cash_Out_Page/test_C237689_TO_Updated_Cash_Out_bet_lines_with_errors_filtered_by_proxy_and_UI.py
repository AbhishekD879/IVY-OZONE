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
class Test_C237689_TO_Updated_Cash_Out_bet_lines_with_errors_filtered_by_proxy_and_UI(Common):
    """
    TR_ID: C237689
    NAME: TO Updated Cash Out bet lines with errors filtered by proxy and UI
    DESCRIPTION: This test case verifies displaying of error messages filtered by proxy during loading and sitting on 'Сash Out' page
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Single and Multiple bets with available cash out
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **cashoutValue filtered by the proxy:**
    PRECONDITIONS: * CASHOUT_SELN_SUSPENDED (need to suspend event/market/selection)
    PRECONDITIONS: * CASHOUT_LINE_NO_CASHOUT ( mock in Fiddler tool)
    PRECONDITIONS: * DB_ERROR ( mock in Fiddler tool)
    PRECONDITIONS: For now there is no known way how to trigger cashoutValue CASHOUT_LINE_NO_CASHOUT and DB_ERROR in OB Backoffice. Fiddler tool can be used to mock responses.
    PRECONDITIONS: How to use Fiddler tool: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+mock+proxy+responses+using+Fiddler
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: *  'Cash Out' tab is opened
        EXPECTED: *  All bets are shown without error messages
        """
        pass

    def test_002_go_to_the_first_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to the first **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_in_ob_backoffice_trigger_cashoutvalue_cashout_line_suspended_in_getbetdetail_response_for_single_cash_out_betsuspend_event_or_market_or_selection_for_event_with_placed_bet(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashoutValue: "CASHOUT_LINE_SUSPENDED" in **getbetDetail** response for **Single** Cash Out bet
        DESCRIPTION: (Suspend event or market or selection for event with placed bet)
        EXPECTED: The error message is displayed instead of 'CASH OUT' and 'Partial CashOut' button with the following information:
        EXPECTED: *   Message of **CASH OUT NOT AVAILABLE** is shown below bet line details. Text of message is centered.
        EXPECTED: *   Underneath the "CASH OUT NOT AVAILABLE" box, another message is displayed: **Your selection is suspended**. Text of message is centered.
        """
        pass

    def test_004_tap_somewhere_else_not_by_message_or_scroll_updown_and_remove_finger(self):
        """
        DESCRIPTION: Tap somewhere else (not by message) or scroll up/down and remove finger
        EXPECTED: Message does not disappear
        """
        pass

    def test_005_navigate_to_another_page_and_return_back_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to another page and return back to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * Single bet is shown with the same error message as in step #3
        EXPECTED: * cashoutValue: "CASHOUT_SELN_SUSPENDED" is received in **getbetDetails** response
        """
        pass

    def test_006_in_ob_backoffice_unsuspend_event(self):
        """
        DESCRIPTION: In OB Backoffice unsuspend event
        EXPECTED: 'CASH OUT' and 'Partial CashOut' buttons are shown under bet details instead of error message
        """
        pass

    def test_007_go_to_second_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to second **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_008_trigger_cashoutvalue_cashout_line_no_cashout_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_tool(self):
        """
        DESCRIPTION: Trigger cashoutValue: "CASHOUT_LINE_NO_CASHOUT" in **getbetDetail** response for **Single** Cash Out bet (e.g. mock response with Fiddler tool)
        EXPECTED: *   Error message of **CASH OUT NOT AVAILABLE** is shown below bet line details instead of 'CASH OUT' button. Text of message is centered.
        """
        pass

    def test_009_verify_errors_displaying_logic(self):
        """
        DESCRIPTION: Verify errors displaying logic
        EXPECTED: * Errors don't disappear after scrolling up and down or collapsing-expanding bet accordion
        EXPECTED: * After 5 seconds **bet with error is removed** from the Cash Out section
        EXPECTED: * After page refresh bet is not displayed on the Cash Out section
        """
        pass

    def test_010_go_to_third_verified_single_cash_out_bet_line_and_move_partial_cashout_slider_to_any_value_not_to_100(self):
        """
        DESCRIPTION: Go to third verified Single Cash Out bet line and move Partial CashOut slider to any value (not to 100%)
        EXPECTED: 
        """
        pass

    def test_011_trigger_cashoutvalue_db_error_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_tool(self):
        """
        DESCRIPTION: Trigger cashoutValue: "DB_ERROR" in getbetDetail response for **Single** Cash Out bet (e.g. mock response with Fiddler tool)
        EXPECTED: *   Error message of **CASH OUT NOT AVAILABLE** is shown below bet line details instead of 'CASH OUT' and 'Partial CashOut' buttons. Text of message is centered.
        """
        pass

    def test_012_go_to_first_multiples_cash_out_bet_line_in_card_view(self):
        """
        DESCRIPTION: Go to first **Multiples** Cash Out bet line in card view
        EXPECTED: 
        """
        pass

    def test_013_in_ob_backoffice_trigger_cashoutvalue_cashout_seln_suspended_in_getbetdetail_response_for_multiple_cash_out_betsuspend_event_or_market_or_selection_for_event_with_placed_bet(self):
        """
        DESCRIPTION: In OB Backoffice trigger cashoutValue: "CASHOUT_SELN_SUSPENDED" in **getbetDetail** response for **Multiple** Cash Out bet
        DESCRIPTION: (Suspend event or market or selection for event with placed bet)
        EXPECTED: The error message is displayed instead of 'CASH OUT' and 'Partial CashOut' buttons with the following information:
        EXPECTED: *   Message of **CASH OUT NOT AVAILABLE** is shown below bet line details. Text of message is centered.
        EXPECTED: *   Underneath the "CASH OUT NOT AVAILABLE" box, another message is displayed: **At least one of your selections is suspended**. Text of message is centered.
        """
        pass

    def test_014_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: * Multiple bet is shown with the same error message as in step #13
        EXPECTED: * cashoutValue: "CASHOUT_SELN_SUSPENDED" is received in **getbetDetails** response
        """
        pass

    def test_015_repeat_steps_8_11_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps #8-11 for Multiple bets
        EXPECTED: Results are the same
        """
        pass

    def test_016_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Bets are shown with relevant error messages (if cashoutStatus filtered by proxy is received in **getbetDetails** response)
        """
        pass
