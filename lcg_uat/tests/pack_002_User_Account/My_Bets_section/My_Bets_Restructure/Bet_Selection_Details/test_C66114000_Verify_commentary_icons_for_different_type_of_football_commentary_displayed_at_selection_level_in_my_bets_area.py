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
class Test_C66114000_Verify_commentary_icons_for_different_type_of_football_commentary_displayed_at_selection_level_in_my_bets_area(Common):
    """
    TR_ID: C66114000
    NAME: Verify commentary icons for different type of football commentary displayed at selection level in my bets area
    DESCRIPTION: This test case is to Verify commentary icons for different type of football commentary displayed at selection level in my bets area
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

    def test_003_go_to_my_bets_and_verify_commentary_icons_for_different_type_of_football_commentary_displayed_at_selection_level_in_my_bets_area(self):
        """
        DESCRIPTION: Go to my bets and Verify commentary icons for different type of football commentary displayed at selection level in my bets area
        EXPECTED: Different commentary icons should be displayed for different commenatry as per the Type of Football commentary
        """
        pass

    def test_004_verify_icons_of_football_commentary_under_open_bets_for_acca_bets(self):
        """
        DESCRIPTION: verify icons of football commentary under open bets for ACCA bets
        EXPECTED: Different commentary icons should be displayed for different commenatry as per the Type of Football commentary at selection level
        """
        pass

    def test_005_repeat_5th_and_6th_step_under_cashout_tab_and_verify(self):
        """
        DESCRIPTION: Repeat 5th and 6th step under cashout tab and verify
        EXPECTED: Result should be same as above
        """
        pass
