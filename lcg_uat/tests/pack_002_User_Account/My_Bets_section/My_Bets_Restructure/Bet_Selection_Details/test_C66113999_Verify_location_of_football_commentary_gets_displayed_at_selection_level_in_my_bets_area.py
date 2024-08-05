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
class Test_C66113999_Verify_location_of_football_commentary_gets_displayed_at_selection_level_in_my_bets_area(Common):
    """
    TR_ID: C66113999
    NAME: Verify location of football commentary gets displayed at selection level in my bets area
    DESCRIPTION: This test case is to Verify location of football commentary gets displayed at selection level in my bets area
    PRECONDITIONS: User should have enough balance to place bets using stake
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_001_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be able to logged in.
        """
        pass

    def test_002_go_to_football_from_sports_ribbon_a_z_menu_and_place_single_and_multiple_bets_from_different_in_play_events(self):
        """
        DESCRIPTION: Go to Football from Sports ribbon/ A-Z menu and place single and multiple bets from different in-play events
        EXPECTED: Should be able to place single and multiple bets from in-play events of football
        """
        pass

    def test_003_go_to_mybets_and_verify_the_location_of_football_commentary_under_open_bets(self):
        """
        DESCRIPTION: Go to mybets and verify the location of football commentary under open bets
        EXPECTED: The location of the football commentary should be displayed below event name  (ex: Team A vs TeamB).  Note: Cashout avialbale bets under open bets only will be display under cashout tab
        """
        pass

    def test_004_go_to_cashout_tab_and_verify_the_location_of_football_commentary_under_cashout_bets(self):
        """
        DESCRIPTION: Go to Cashout tab and verify the location of football commentary under cashout bets
        EXPECTED: The location of the football commentary should be displayed below event name  (ex: Team A vs TeamB).  Note: Cashout avialbale bets under open bets only will be display under cashout tab
        """
        pass

    def test_005_verify_the_location_of_football_commentary_under_open_bets_for_acca_bets(self):
        """
        DESCRIPTION: verify the location of football commentary under open bets for ACCA bets
        EXPECTED: The location of the football commentary should be displayed below event name  (ex: Team A vs TeamB) at selection level.
        """
        pass

    def test_006_repeat_6th_step_under_cashout_tab_and_verify(self):
        """
        DESCRIPTION: Repeat 6th step under cashout tab and verify
        EXPECTED: Result should be same as above
        """
        pass
