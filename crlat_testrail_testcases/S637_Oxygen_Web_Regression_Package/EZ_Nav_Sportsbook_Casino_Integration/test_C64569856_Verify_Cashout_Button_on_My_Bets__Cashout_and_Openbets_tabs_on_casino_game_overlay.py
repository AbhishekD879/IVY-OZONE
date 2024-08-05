import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64569856_Verify_Cashout_Button_on_My_Bets__Cashout_and_Openbets_tabs_on_casino_game_overlay(Common):
    """
    TR_ID: C64569856
    NAME: Verify Cashout Button on My Bets -> Cashout and Openbets tabs on casino game overlay.
    DESCRIPTION: Verify Cashout Button on My Bets -&gt; Cashout and Openbets tabs on casino game overlay.
    PRECONDITIONS: * Cashout Tab is enabled from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User has placed Singles and Multiple bets where Cash Out offer is available
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User navigates to 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_tap_cashout_tab(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        EXPECTED: * Cashoutable bets are loaded
        EXPECTED: * User able to see Cashout button on the selection
        """
        pass

    def test_004_go_to_single_bets_gt_tap_cash_out_buttonverify_that_green_confirm_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Go to 'Single' bets-&gt; Tap 'CASH OUT' button
        DESCRIPTION: Verify that green 'CONFIRM CASH OUT' button is shown
        EXPECTED: * 'CONFIRM CASH OUT' button is shown
        """
        pass

    def test_005_tap_confirm_cash_out_button(self):
        """
        DESCRIPTION: Tap 'CONFIRM CASH OUT' button
        EXPECTED: * Inplay events:
        EXPECTED: Spinner with count down timer in format of XX:XX (countdown timer is taken from 'cashoutBet' response: 'cashoutDelay attribute value)
        EXPECTED: * Preplay events:
        EXPECTED: Spinner
        EXPECTED: Cashing Out label should display for preplay events
        """
        pass

    def test_006_wait_until_button_with_spinner_and_count_down_timer_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner and count down timer disappears
        EXPECTED: * 'Cashed out' label is displayed at the top right corner on the header
        EXPECTED: * Green "tick" in a circle and message "You cashed out " is shown below the header
        EXPECTED: * Message "Cash Out Successful" with the green tick at the beginning are shown instead of 'cashout' button at the bottom of bet line
        """
        pass

    def test_007_repeat_steps_4_6_for_multiple_bets_in_cashout_tab(self):
        """
        DESCRIPTION: Repeat steps 4-6 for 'Multiple' bets in cashout tab
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_7_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat steps 3-7 in 'Openbets' tab
        EXPECTED: 
        """
        pass
