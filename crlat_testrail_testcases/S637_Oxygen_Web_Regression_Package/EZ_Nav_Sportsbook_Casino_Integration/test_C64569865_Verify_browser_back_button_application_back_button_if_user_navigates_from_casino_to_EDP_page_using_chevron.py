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
class Test_C64569865_Verify_browser_back_button_application_back_button_if_user_navigates_from_casino_to_EDP_page_using_chevron(Common):
    """
    TR_ID: C64569865
    NAME: Verify browser back button & application back button if user navigates from casino to EDP page using chevron.
    DESCRIPTION: Verify browser back button & application back button if user navigates from casino to EDP page using chevron.
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

    def test_004_tap_go_to_sports_cta(self):
        """
        DESCRIPTION: Tap 'GO TO SPORTS' CTA
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_005_tap_on_yes_lets_go_cta(self):
        """
        DESCRIPTION: Tap on 'YES, LET'S GO' CTA
        EXPECTED: * User navigates to sportsbook homepage
        """
        pass

    def test_006_click_browser_back_button(self):
        """
        DESCRIPTION: Click browser back button
        EXPECTED: * User navigates back to Casino from Sportsbook.
        """
        pass

    def test_007_again_open_mybets_overlay_by_tapping_on_sports_icon_at_eznav_panel(self):
        """
        DESCRIPTION: Again open MYBETS overlay by tapping on sports icon at eznav panel
        EXPECTED: * User is on MYBETS overlay
        """
        pass

    def test_008_tap_on_edp_chevronbottom_quicklinksgo_to_5a_side_leaderboardgo_to_5a_side_cta(self):
        """
        DESCRIPTION: Tap on EDP chevron/bottom quicklinks/Go to 5A-side leaderboard/Go to 5A-side CTA
        EXPECTED: * A confirmation popup with CTA should be displayed - stating that: 'Are you sure you want to end your gaming session and visit Sportsbook?'
        EXPECTED: 1. NO THANKS
        EXPECTED: 2. YES, LET'S GO(Yellow background)
        EXPECTED: 3. Do not show me this message again(checkbox)
        """
        pass

    def test_009_tap_on_yes_lets_go_cta(self):
        """
        DESCRIPTION: Tap on 'YES, LET'S GO' CTA
        EXPECTED: * User navigates to its corresponding page
        """
        pass

    def test_010_click_application_back_button(self):
        """
        DESCRIPTION: Click application back button
        EXPECTED: * User navigates to sportsbook homepage
        """
        pass

    def test_011_now_come_back_to_gaming_page_gtmybets_overlay_repeat_step_45678910_in_all__openbetssettledbets_inner_tabs(self):
        """
        DESCRIPTION: Now come back to Gaming page-&gt;MyBets Overlay Repeat step-4,5,6,7,8,9,10 in all  Openbets/Settledbets inner tabs
        EXPECTED: 
        """
        pass
