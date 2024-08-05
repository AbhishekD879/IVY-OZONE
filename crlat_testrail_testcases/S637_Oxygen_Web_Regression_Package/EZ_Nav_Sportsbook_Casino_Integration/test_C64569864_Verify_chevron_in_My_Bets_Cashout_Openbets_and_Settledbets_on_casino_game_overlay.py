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
class Test_C64569864_Verify_chevron_in_My_Bets_Cashout_Openbets_and_Settledbets_on_casino_game_overlay(Common):
    """
    TR_ID: C64569864
    NAME: Verify chevron in My Bets-> Cashout, Openbets and Settledbets on casino game overlay.
    DESCRIPTION: Verify chevron in My Bets-&gt; Cashout, Openbets and Settledbets on casino game overlay.
    PRECONDITIONS: * Cashout Tab should be enable from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User should have open bets & settled bets
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

    def test_004_tap_on_any_bet_or_chevron(self):
        """
        DESCRIPTION: Tap on any bet or chevron
        EXPECTED: * Bet is clickable
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_005_tap_on_yes_lets_go_cta(self):
        """
        DESCRIPTION: Tap on 'YES, LET'S GO' CTA
        EXPECTED: * User navigates to its corresponding EDP page
        """
        pass

    def test_006_6_now_come_back_to_gaming_page_gtmybets_overlay_repeat_step_45_in_all__openbetssettledbets_inner_tabs_wherever_there_is_a_possibility_for_the_user(self):
        """
        DESCRIPTION: 6. Now come back to Gaming page-&gt;MyBets Overlay Repeat step-4,5 in all  Openbets/Settledbets inner tabs wherever there is a possibility for the user
        EXPECTED: 
        """
        pass