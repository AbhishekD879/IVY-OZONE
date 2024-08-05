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
class Test_C237154_Successful_Full_Cash_Out_process_for_Preplay_and_Inplay_events(Common):
    """
    TR_ID: C237154
    NAME: Successful Full Cash Out process for Preplay and Inplay events
    DESCRIPTION: This test case verifies successful Full Cash Out process on 'Cash Out' tab
    DESCRIPTION: NOTE:
    DESCRIPTION: Spinner + Count down timer should display on clicking on 'Cashout' for Inplay event
    DESCRIPTION: Spinner + Cashing out label should display on clicking on 'Cashout' for preplay event
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: **CORAL**
    PRECONDITIONS: Delay for Singles and Multiple bets is set in the backoffice/admin -> Miscellaneous -> Openbet Config -> All Configuration groups -> CASHOUT_SINGLE_DELAY / CASHOUT_MULTI_DELAY
    PRECONDITIONS: Configurable Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: Cashout values are used in "cashoutDelay" attribute in 'cashoutBet' response, the calculation is based on the BIR delay in the event (pre-play bets won't be a cashout delay, use only In-Play events for testing Timer, (Timer is available from OX 99))
    PRECONDITIONS: The highest set 'BIR Delay' value is used for Multiples In-play events
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Cash Out page;
    PRECONDITIONS: - Open Bets page;
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_002_go_to_single_cash_out_bet_line(self):
        """
        DESCRIPTION: Go to **Single** Cash Out bet line
        EXPECTED: 
        """
        pass

    def test_003_tap_cash_out_buttonverify_that_green_confirm_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' button is shown
        EXPECTED: 'CONFIRM CASH OUT' button is shown
        """
        pass

    def test_004_trigger_happy_cash_out_path_eg_cash_out_valueremains_unchanged(self):
        """
        DESCRIPTION: Trigger happy cash out path (e.g. cash out value remains unchanged)
        EXPECTED: 
        """
        pass

    def test_005_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: Inplay events:
        EXPECTED: Spinner with count down timer (Timer is available from OX 99) in format XX:XX (countdown timer is taken from 'cashoutBet' response: 'cashoutDelay attribute value)
        EXPECTED: ![](index.php?/attachments/get/122292614)
        EXPECTED: Preplay events:
        EXPECTED: Spinner + Cashing Out label should display for preplay events
        EXPECTED: ![](index.php?/attachments/get/122292613)
        """
        pass

    def test_006_wait_untilbutton_with_spinner_and_count_down_timer__timer_is_available_from_ox_99disappears(self):
        """
        DESCRIPTION: Wait until button with spinner and count down timer  (Timer is available from OX 99)
        DESCRIPTION: disappears
        EXPECTED: * 'Cashed out' label is displayed at the top right corner on the header
        EXPECTED: *   Green "tick" in a circle and message "You cashed out <currency> <value>" is shown below the header
        EXPECTED: * Message "Cash Out Successful" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        EXPECTED: ![](index.php?/attachments/get/122292660)
        """
        pass

    def test_007_verify_user_balance(self):
        """
        DESCRIPTION: Verify user balance
        EXPECTED: User balance is increased on full cash out value
        """
        pass

    def test_008_refresh_the_page_or_navigate_to_other_page_and_backverify_success_message(self):
        """
        DESCRIPTION: Refresh the page (or navigate to other page and back)
        DESCRIPTION: Verify success message
        EXPECTED: The success message and bet are no longer displayed
        """
        pass

    def test_009_go_to_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Go to **Multiple** Cash Out bet lines
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_9_for_multiple_cash_out_bet_lines(self):
        """
        DESCRIPTION: Repeat steps 3-9 for **Multiple** Cash Out bet lines
        EXPECTED: 
        """
        pass

    def test_011__change_cashout_delays_values_coral_for_singles_and_multiples_in_ob_and_bir_delays_values_ladbrokes_for_the_in_play_events_available_from_ox_99_repeat_steps_3_10(self):
        """
        DESCRIPTION: * Change Cashout Delays values (Coral) for Singles and Multiples in OB and BIR Delays values (Ladbrokes) for the In-play events (available from OX 99)
        DESCRIPTION: * Repeat steps 3-10
        EXPECTED: 
        """
        pass
