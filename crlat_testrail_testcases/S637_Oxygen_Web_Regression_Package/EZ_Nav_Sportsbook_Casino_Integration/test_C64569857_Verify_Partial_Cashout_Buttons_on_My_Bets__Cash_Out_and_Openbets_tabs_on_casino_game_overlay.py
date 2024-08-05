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
class Test_C64569857_Verify_Partial_Cashout_Buttons_on_My_Bets__Cash_Out_and_Openbets_tabs_on_casino_game_overlay(Common):
    """
    TR_ID: C64569857
    NAME: Verify Partial Cashout Buttons on My Bets -> Cash Out and Openbets tabs on casino game overlay.
    DESCRIPTION: Verify Partial Cashout Buttons on My Bets -&gt; Cash Out and Openbets tabs on casino game overlay.
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
        EXPECTED: * User able to see partial Cashout button on the selection
        """
        pass

    def test_004_go_to_single_bets_gt_click_on_partial_cashout_button_on_cashout_bar(self):
        """
        DESCRIPTION: Go to 'Single' bets-&gt; Click on 'Partial CashOut' button on CashOut bar
        EXPECTED: * 'Partial CashOut' slider is shown
        """
        pass

    def test_005_set_pointer_on_the_bar_to_any_value_not_to_maximum(self):
        """
        DESCRIPTION: Set pointer on the bar to any value (not to maximum)
        EXPECTED: * Value on CashOut button is changed
        """
        pass

    def test_006_tap_cash_out_buttonverify_that__confirm_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button
        DESCRIPTION: Verify that  'CONFIRM CASH OUT' button is shown
        EXPECTED: * 'CONFIRM CASH OUT' button is shown & it blinks for 3 times then back to 'CASH OUT' button
        """
        pass

    def test_007_tap_cash_out_button_again_and_confirm_cashout(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button again and confirm cashout
        EXPECTED: * Inplay events:
        EXPECTED: Spinner with count down timer in format of XX:XX (countdown timer is taken from 'cashoutBet' response: 'cashoutDelay attribute value)
        EXPECTED: * Preplay events:
        EXPECTED: Spinner
        EXPECTED: Cashing Out label should display for preplay events
        """
        pass

    def test_008_wait_until_button_with_spinner_and_count_down_timer_disappears(self):
        """
        DESCRIPTION: Wait until button with spinner and count down timer disappears
        EXPECTED: *The success message is displayed below 'CASH OUT' button i.e., "Partial Cashout Successful"
        EXPECTED: * Stake and Est. Returns values are decreased within bet accordion and bet line, new values are shown
        """
        pass

    def test_009_repeat_steps_4_8_for_multiple_bets_in_cashout_tab(self):
        """
        DESCRIPTION: Repeat steps 4-8 for 'Multiple' bets in cashout tab
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_9_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat steps 3-9 in 'Openbets' tab
        EXPECTED: 
        """
        pass
