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
class Test_C64569850_Verify_Go_To_Sports_CTA_on_the_Gaming_overlay(Common):
    """
    TR_ID: C64569850
    NAME: Verify 'Go To Sports' CTA on the Gaming overlay.
    DESCRIPTION: Verify 'Go To Sports' CTA on the Gaming overlay.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in.
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
        EXPECTED: * User navigates to 'MyBets' overlay displays 'Go To Sports' CTA in openbets, cashout, settledbets inner tabs(sports, lotto, pools) at bottom of the page.
        """
        pass

    def test_003_tap_on_go_to_sports_cta_on_the_overlay(self):
        """
        DESCRIPTION: Tap on 'Go To Sports' CTA on the overlay
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_004_tap_on_no_thanks(self):
        """
        DESCRIPTION: Tap on 'NO THANKS'
        EXPECTED: * Pop up is closed & user is in MyBets page
        """
        pass

    def test_005_now_tap_on_go_to_sports_cta_on_the_overlay__tap_on_yes_lets_go(self):
        """
        DESCRIPTION: Now Tap on 'Go To Sports' CTA on the overlay & Tap on 'YES, LET'S GO'
        EXPECTED: * User redirects to sportsbook homepage
        """
        pass

    def test_006_repeat_step_1_step_2_step_3___check_the_do_not_show_me_this_message_again_checkbox_then_tap_no_thanks(self):
        """
        DESCRIPTION: Repeat step-1, step-2, step-3  & check the 'Do not show me this message again' checkbox then Tap 'NO THANKS'
        EXPECTED: * User checked the checkbox
        EXPECTED: * User will be on same page i.e., My Bets page
        """
        pass

    def test_007_atlast_tap_on_go_to_sports_cta_on_the_overlay(self):
        """
        DESCRIPTION: Atlast Tap on 'Go To Sports' CTA on the overlay
        EXPECTED: * User won't get popup & directly navigates to sportsbook homepage
        """
        pass
