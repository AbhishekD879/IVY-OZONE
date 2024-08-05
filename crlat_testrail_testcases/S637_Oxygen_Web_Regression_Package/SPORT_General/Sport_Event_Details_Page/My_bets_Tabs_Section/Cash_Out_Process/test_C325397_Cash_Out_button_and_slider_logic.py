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
class Test_C325397_Cash_Out_button_and_slider_logic(Common):
    """
    TR_ID: C325397
    NAME: Cash Out button and slider logic
    DESCRIPTION: The test case needs to be edited according to the latest changes+Vanilla changes.
    DESCRIPTION: This test case verifies Cash Out button and slider logic on 'My Bets' tab on Event Details page
    DESCRIPTION: *Jira Tickets:*
    DESCRIPTION: [BMA-24365 My Bets Improvement : CashOut: Redesign of main cashout CTA Partial Cashout] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24365
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: * In order to trigger unavailable Partial Cash Out place a bet with small amount
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * 'PARTIAL CASHOUT' slider is not shown
        """
        pass

    def test_002__navigate_to_single_bet_line_click_on_the_cash_out_currency_symbolvalue_button_and_wait(self):
        """
        DESCRIPTION: * Navigate to **Single** bet line
        DESCRIPTION: * Click on the 'CASH OUT <currency symbol><value>' button and wait
        EXPECTED: * Button updates with the following centered text 'CONFIRM CASH OUT: <currency symbol><value>' and becomes green
        EXPECTED: * 'PARTIAL CASHOUT' is disappeared from CASHOUT bar
        EXPECTED: * The Cash Out button displays with 'CONFIRM CASH OUT' for a maximum of 6200ms
        EXPECTED: * 'Confirm Cash Out' button flashes three times when time is running out
        EXPECTED: * 'Confirm Cash Out' button has expired, becomes 'Cash Out <currency symbol><value>' button until user clicks on Cash Out button again
        EXPECTED: * Cash Out and Partial CashOut buttons revert to normal and are updated to the correct value/status
        EXPECTED: **Note:** Old pop-up with confirmation message doesn't appear
        """
        pass

    def test_003_1_click_on_the_cash_out_currency_symbolvalue_button_and_trigger_error_cashout_seln_suspended_for_bet_via_liveserve_update_suspend_event_or_market_or_selection_for_event_with_placed_bet2_click_cashout_button_confirm_cashout_and_simultaneously_trigger_cashoutvalue_cashout_seln_no_cashout_in_getbetdetail_response_for_single_cash_out_bet_eg_mock_response_with_fiddler_tool(self):
        """
        DESCRIPTION: 1) Click on the 'CASH OUT <currency symbol><value>' button and trigger error "CASHOUT_SELN_SUSPENDED" for bet via LiveServe update (Suspend event or market or selection for event with placed bet)
        DESCRIPTION: 2) Click 'Cashout' button, confirm cashout and simultaneously trigger cashoutValue: "CASHOUT_SELN_NO_CASHOUT" in getbetDetail response for Single Cash Out bet (e.g. mock response with Fiddler tool)
        EXPECTED: Flashing stops and error is shown immediately as described in TC 238033 or TC 237389
        """
        pass

    def test_004_click_on_the_cash_out_button_and_click_on_confirm_cash_out(self):
        """
        DESCRIPTION: Click on the 'CASH OUT' button and click on 'CONFIRM CASH OUT'
        EXPECTED: * The Cash Out attempt is sent to OpenBet (cashoutBet request is sent, can be checked in Network tab)
        EXPECTED: * Spinner is displayed centered
        """
        pass

    def test_005__navigate_to_another_single_bet_click_on_partial_cashout_button_and_move_slider_on_the_bar(self):
        """
        DESCRIPTION: * Navigate to another Single bet
        DESCRIPTION: * Click on 'PARTIAL CASHOUT' button and move slider on the bar
        EXPECTED: * Pointer on the Bar moves left or right
        EXPECTED: * Value on CashOut button is changed
        """
        pass

    def test_006_set_pointer_on_the_slider_to_any_percentage_value_and_refresh_page(self):
        """
        DESCRIPTION: Set pointer on the slider to any percentage value and refresh page
        EXPECTED: 'CASH OUT <currency symbol><value>' and 'PARTIAL CASHOUT' are seen on CASHOUT bar
        """
        pass

    def test_007_set_pointer_on_the_slider_to_any_percentage_value_and_navigate_to_other_pagetabnavigate_back_to_my_bets_tab_on_event_details_page(self):
        """
        DESCRIPTION: Set pointer on the slider to any percentage value and navigate to other page/tab
        DESCRIPTION: Navigate back to 'My Bets' tab on Event Details page
        EXPECTED: 'CASH OUT <currency symbol><value>' and 'PARTIAL CASHOUT' are seen on CASHOUT bar
        """
        pass

    def test_008_navigate_to_bet_line_with_unavailable_partial_cash_out(self):
        """
        DESCRIPTION: Navigate to bet line with unavailable Partial Cash Out
        EXPECTED: 'PARTIAL CASHOUT' button is not shown on CASHOUT bar
        """
        pass

    def test_009_repeat_steps_2_8_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-8 for **Multiple** bet
        EXPECTED: 
        """
        pass
