import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.cash_out
@vtest
class Test_C237690_Successful_Partial_Cash_Out_process(Common):
    """
    TR_ID: C237690
    NAME: Successful Partial Cash Out process
    DESCRIPTION: This test case verifies successful Partial Cash Out process on 'Cash Out' tab
    DESCRIPTION: DESIGNS (available from OX 99):
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f1ce639594ebeef05d0cc
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f09b1d2815d60d0789631
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: **CORAL**
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of of pre-match events. (Currently works as for in-play events)
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab (if available);
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Cash Out page;
    PRECONDITIONS: - Open Bets page.
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - WebSocket connection to Cashout MS should be created when user lands on Cashout tab/OpenBets page
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_outopen_bets_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out/Open Bets' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out/Open Bets' tab is opened
        """
        pass

    def test_002_find_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Find **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_click_on_partial_cashout_button_on_cashout_bar(self):
        """
        DESCRIPTION: Click on 'Partial CashOut' button on CashOut bar
        EXPECTED: 'Partial CashOut' slider is shown
        """
        pass

    def test_004_set_pointer_on_the_bar_to_any_value_not_to_maximum(self):
        """
        DESCRIPTION: Set pointer on the bar to any value (not to maximum)
        EXPECTED: Value on CashOut button is changed
        """
        pass

    def test_005_tap_cash_out_buttonverify_that__confirm_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that  'CONFIRM CASH OUT' button is shown
        EXPECTED: 'CONFIRM CASH OUT' button is shown
        """
        pass

    def test_006_trigger_happy_cash_out_path_eg_cash_out_value_remains_unchanged_and_confirm_cashout(self):
        """
        DESCRIPTION: Trigger happy cash out path (e.g. cash out value remains unchanged) and confirm cashout
        EXPECTED: Spinner icon with countdown timer  (Timer is available from OX 99) in format XX:XX (countdown timer is taken from 'cashoutBet' response: 'cashoutDelay attribute value)
        EXPECTED: appears on the button instead of the text 'CONFIRM CASH OUT'
        """
        pass

    def test_007_wait_until_button_with_spinner_and_countdown_timer_disappears_timer_is_available_from_ox_99(self):
        """
        DESCRIPTION: Wait until button with spinner and countdown timer disappears (timer is available from OX 99)
        EXPECTED: * The success message is displayed below 'CASH OUT' button
        EXPECTED: "Partial Cashout Successful"
        EXPECTED: * Stake and Est. Returns values are decreased within bet accordion and bet line, new values are shown
        EXPECTED: ![](index.php?/attachments/get/33903)
        """
        pass

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on previously cashed out value
        """
        pass

    def test_009_navigate_to_multiple_cash_out_bet_line(self):
        """
        DESCRIPTION: Navigate to **Multiple** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_10_for_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Repeat steps #3-10 for Multiple Cash Out bet lines
        EXPECTED: 
        """
        pass
