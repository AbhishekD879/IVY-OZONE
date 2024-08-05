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
class Test_C237766_Successful_Partial_Cash_Out_process(Common):
    """
    TR_ID: C237766
    NAME: Successful Partial Cash Out process
    DESCRIPTION: This test case verifies successful Partial Cash Out process on 'My Bets' tab on Event Details page
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Readbet request/response is sent after successful partial cashout of in-play events.
    PRECONDITIONS: CashoutBet request/response is sent after successful partial cashout of pre-match events. (Currently, works as for in-play events)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Single** bet with available cash out
        EXPECTED: 'My Bets' tab is opened
        """
        pass

    def test_002_tap_on_partial_cashout_button(self):
        """
        DESCRIPTION: Tap on 'Partial CashOut' button
        EXPECTED: 'Partial CashOut' slider appears
        """
        pass

    def test_003_set_pointer_on_the_slider_to_any_percentage_value_not_to_100(self):
        """
        DESCRIPTION: Set pointer on the slider to any percentage value (not to 100%)
        EXPECTED: Pointer is set on the certain value
        """
        pass

    def test_004_tap_cash_out_button_eg_cash_out_value_remains_unchanged(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button (e.g. cash out value remains unchanged)
        EXPECTED: 
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
        EXPECTED: * 'Partial cashout successful' message is displayed blow the cashout button with the green tick icon
        EXPECTED: * Stake and Est. Returns values are decreased within bet accordion and bet line, new values are shown
        """
        pass

    def test_007_verify_success_message_animation(self):
        """
        DESCRIPTION: Verify success message animation
        EXPECTED: The success message:
        EXPECTED: * fades in for 200 ms
        EXPECTED: * is displayed for 3000 ms
        EXPECTED: * fades out for 700 ms
        EXPECTED: Once the success message completely fades out 'CASH OUT' button with new cash out value and slider set to 100% appear again
        """
        pass

    def test_008_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on previously cashed out value
        """
        pass

    def test_009_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bets with available cash out
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_9_for_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Repeat steps #2-9 for Multiple Cash Out bet lines
        EXPECTED: 
        """
        pass
