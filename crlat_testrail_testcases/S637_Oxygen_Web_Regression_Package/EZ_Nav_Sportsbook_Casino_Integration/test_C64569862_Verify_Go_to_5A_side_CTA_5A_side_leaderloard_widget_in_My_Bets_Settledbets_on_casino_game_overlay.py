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
class Test_C64569862_Verify_Go_to_5A_side_CTA_5A_side_leaderloard_widget_in_My_Bets_Settledbets_on_casino_game_overlay(Common):
    """
    TR_ID: C64569862
    NAME: Verify 'Go to 5A-side' CTA & '5A-side leaderloard' widget in My Bets->Settledbets on casino game overlay.
    DESCRIPTION: Verify 'Go to 5A-side' CTA & '5A-side leaderloard' widget in My Bets-&gt;Settledbets on casino game overlay.
    PRECONDITIONS: * Cashout Tab is enabled from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User has placed bets on 5A-Side & it is shown in 'Settled bets' tab
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

    def test_003_tap_settled_betsverify_5a_side_void_bets_if_contest_is_active__inactive(self):
        """
        DESCRIPTION: Tap 'Settled Bets'
        DESCRIPTION: Verify 5A-Side VOID bets if contest is active & inactive
        EXPECTED: * Settled bets are loaded
        EXPECTED: * User able to see 5A-Side VOID bets in below format:
        EXPECTED: '5A-side leaderboard' widget if contest is active
        EXPECTED: 'Go to 5A-side' button if contest is inactive
        """
        pass

    def test_004_tap_on_5a_side_leaderboard_widget(self):
        """
        DESCRIPTION: Tap on '5A-side leaderboard' widget
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_005_tap_no_thanks(self):
        """
        DESCRIPTION: Tap 'NO THANKS'
        EXPECTED: * User will stay on same page i.e., Settled Bets
        """
        pass

    def test_006_tap_on_go_to_5a_side_button(self):
        """
        DESCRIPTION: Tap on 'GO TO 5A-SIDE' button
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass
