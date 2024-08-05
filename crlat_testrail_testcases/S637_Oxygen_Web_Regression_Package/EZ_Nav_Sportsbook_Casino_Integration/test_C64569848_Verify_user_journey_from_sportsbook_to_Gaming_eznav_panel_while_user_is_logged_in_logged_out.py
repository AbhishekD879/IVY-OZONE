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
class Test_C64569848_Verify_user_journey_from_sportsbook_to_Gaming_eznav_panel_while_user_is_logged_in_logged_out(Common):
    """
    TR_ID: C64569848
    NAME: Verify user journey from sportsbook to Gaming eznav panel while user is logged in & logged out.
    DESCRIPTION: Verify user journey from sportsbook to Gaming eznav panel while user is logged in & logged out
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_the_sportsbook_application__log_in(self):
        """
        DESCRIPTION: Launch the sportsbook application & log in.
        EXPECTED: *Sportsbook Application is launched
        EXPECTED: *User is logged in sportsbook
        """
        pass

    def test_002_tap_gamingcasino_icon_from_the_footer_menu(self):
        """
        DESCRIPTION: Tap 'Gaming/Casino' icon from the footer menu
        EXPECTED: * User redirects to gaming window
        EXPECTED: * User is logged in gaming window
        """
        pass

    def test_003_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_004_get_back_to_sportsbook__log_out(self):
        """
        DESCRIPTION: Get back to sportsbook & log out
        EXPECTED: * User navigates to Sportsbook page
        EXPECTED: * User is logged out
        """
        pass

    def test_005_again_tap_gamingcasino_icon_from_footer_menu(self):
        """
        DESCRIPTION: Again tap 'Gaming/Casino' icon from footer menu
        EXPECTED: * User redirects to gaming window
        """
        pass

    def test_006_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * Log in pop up is shown
        """
        pass

    def test_007_log_in_to_the_gaming_section__launch_any_casino_game(self):
        """
        DESCRIPTION: Log in to the gaming section & launch any casino game
        EXPECTED: * User is logged in gaming window
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass
