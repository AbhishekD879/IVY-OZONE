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
class Test_C237854_Cash_Out_button_and_slider_logic(Common):
    """
    TR_ID: C237854
    NAME: Cash Out button and slider logic
    DESCRIPTION: This test case verifies Cash Out button and slider logic on Cash Out/Open Bets tab
    DESCRIPTION: DESIGNS (available from OX 99):
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f1ce639594ebeef05d0cc
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f09b1d2815d60d0789631
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: * In order to trigger unavailable Partial Cash Out place a bet with small amount
    PRECONDITIONS: **CORAL**
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab (if available);
    PRECONDITIONS: - Open Bets tab;
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_outopen_bets_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out/Open Bets' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Cash Out/Open Bets' tab is opened
        EXPECTED: * 'CASHOUT','PARTIAL CASHOUT' buttons are displayed
        EXPECTED: * slider of partial cash out is hidden
        """
        pass

    def test_002_click_on_the_cash_out_currency_symbolvalue_button_and_wait(self):
        """
        DESCRIPTION: Click on the 'CASH OUT <currency symbol><value>' button and wait
        EXPECTED: * Button updates with the following centered text 'CONFIRM CASH OUT: <currency symbol><value>'
        EXPECTED: * 'PARTIAL CASHOUT' button disappears from CASHOUT bar
        EXPECTED: * The Cash Out button displays 'CONFIRM CASH OUT' for a maximum of 6200ms
        EXPECTED: * The Cash Out button flashes three times when time is running out
        EXPECTED: * 'Confirm Cash Out' button expires, becomes 'Cash Out <currency symbol><value>' button until user clicks on Cash Out button again
        EXPECTED: * 'Cash Out' and 'Partial CashOut' buttons are displayed again
        """
        pass

    def test_003_check_the_error_in_response_while_waiting_after_pressing_cashout_button(self):
        """
        DESCRIPTION: Check the error in response while waiting after pressing 'cashout' button
        EXPECTED: Flashing stops and error is shown in Network: request 'cashoutBet'-> bet Error: 'CASHOUT_PENDING'
        """
        pass

    def test_004_click_on_the_cash_out_button_and_click_on_confirm_cash_out(self):
        """
        DESCRIPTION: Click on the 'CASH OUT' button and click on 'CONFIRM CASH OUT'
        EXPECTED: * The Cash Out attempt is sent to OpenBet (cashoutBet request is sent, can be checked in Network tab)
        EXPECTED: * Spinner with countdown timer  (Timer is available from OX 99) in format XX:XX is displayed centered instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_005_navigate_to_another_single_bet_and_click_on_partial_cashout_button(self):
        """
        DESCRIPTION: Navigate to another Single bet and click on 'PARTIAL CASHOUT' button
        EXPECTED: 'PARTIAL CASHOUT' slider appears
        """
        pass

    def test_006_click_on_x_button_on_cashout_bar(self):
        """
        DESCRIPTION: Click on 'X' button on CASHOUT bar
        EXPECTED: * 'PARTIAL CASHOUT' slider is hidden
        EXPECTED: * 'CASH OUT <currency symbol><value>' button is shown instead
        EXPECTED: * 'PARTIAL CASHOUT' is shown on CASHOUT bar
        """
        pass

    def test_007_click_on_partial_cashout_button_again(self):
        """
        DESCRIPTION: Click on 'PARTIAL CASHOUT' button again
        EXPECTED: 'PARTIAL CASHOUT' slider appears
        """
        pass

    def test_008_move_slider(self):
        """
        DESCRIPTION: Move slider
        EXPECTED: * The 'Pointer'moves on the Bar
        EXPECTED: * The Cash Out value is automatically updated in the Cash Out button
        EXPECTED: * Partial Cash Out value is rounded to the nearest 2 decimal places
        """
        pass

    def test_009_set_pointer_on_the_bar_to_any_value_and_refresh_page(self):
        """
        DESCRIPTION: Set pointer on the bar to any value and refresh page
        EXPECTED: * Partial CashOut slider is hidden
        EXPECTED: * 'CASH OUT <currency symbol><value>' and 'PARTIAL CASHOUT' buttons are shown instead
        """
        pass

    def test_010_set_pointer_on_the_bar_to_any_value_and_navigate_to_other_pagetabnavigate_back_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Set pointer on the bar to any value and navigate to other page/tab.
        DESCRIPTION: Navigate back to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget.
        EXPECTED: Partial CashOut slider is hidden for all bets on page
        """
        pass

    def test_011_navigate_to_bet_line_with_unavailable_partial_cash_out(self):
        """
        DESCRIPTION: Navigate to bet line with unavailable Partial Cash Out
        EXPECTED: 'PARTIAL CASHOUT' button is not shown on CASHOUT bar
        """
        pass

    def test_012_repeat_steps_2_11_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-11 for **Multiple** bet
        EXPECTED: 
        """
        pass
