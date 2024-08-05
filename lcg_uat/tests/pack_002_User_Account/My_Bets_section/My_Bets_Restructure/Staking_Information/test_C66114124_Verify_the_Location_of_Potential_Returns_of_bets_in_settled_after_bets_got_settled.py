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
class Test_C66114124_Verify_the_Location_of_Potential_Returns_of_bets_in_settled_after_bets_got_settled(Common):
    """
    TR_ID: C66114124
    NAME: Verify the Location of Potential Returns of bets in settled after bets got settled
    DESCRIPTION: This test case is to verify the location of Potential returns of bets after got settled once race/event end
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        pass

    def test_001_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        pass

    def test_002_navigate_to_any_sport_landing_page_from_sports_ribbon_a_z_menu(self):
        """
        DESCRIPTION: Navigate to any sport landing page from sports ribbon /A-Z menu
        EXPECTED: User should be able to navigate to SLP
        """
        pass

    def test_003_place_single_and_mutiple_bets_from_different_in_play_events(self):
        """
        DESCRIPTION: Place single and mutiple bets from different in-play events
        EXPECTED: Single and multiple bets should be placed successfully
        """
        pass

    def test_004_go_to_my_bets_and_verify_recently_placed_bets_under_open(self):
        """
        DESCRIPTION: Go to my bets and verify recently placed bets under open
        EXPECTED: Should be match the bet details under open with recently placed single/multiple bets
        EXPECTED: Note: Bets will be in expanded state by default
        """
        pass

    def test_005_navigate_to_cashout_tab_and_verify_recently_placed_bets(self):
        """
        DESCRIPTION: Navigate to cashout tab and verify recently placed bets
        EXPECTED: Recently placed bets which have cashout under open will be display under cashout
        EXPECTED: Note: The bets which are in open  won't be displayed under cash out if any bet doesn't have cashout avaialble
        """
        pass

    def test_006_navigate_to_settled_once_the_event_is_completed_and_verify_location_of_potential_returns_for_the_bets(self):
        """
        DESCRIPTION: Navigate to settled once the event is completed and verify location of potential returns for the bets
        EXPECTED: User should be able to navigate to settled and can see settled bets and Location of the potential returns should be displayed in line with odds and right justified within the staking area
        EXPECTED: ![](index.php?/attachments/get/69edcdfc-f23c-4da8-9b0d-3e4fefe57138)
        """
        pass

    def test_007_click_on_anywhere_on_the_bet_header_to_collapse_the_bet_and_verify(self):
        """
        DESCRIPTION: Click on anywhere on the bet header to collapse the bet and verify
        EXPECTED: User should be able to collapse bet by clicking on bet header
        """
        pass

    def test_008_verify_the_location_of_the_potential_returns_for_recently_placed_bet_after_collapsing_the_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet after collapsing the bet
        EXPECTED: Location of the potential returns should be displayed in line with stake and right side alligned
        EXPECTED: ![](index.php?/attachments/get/88e63b2f-d8ab-46fc-837d-f790852afee2)
        """
        pass

    def test_009_repeat_step_3_to_step_9_by_placing_bets_in_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat step 3 to step 9 by placing bets in lottos and pools along with races
        EXPECTED: Result will be same as above
        """
        pass
