import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64368258_Verify_the_back_button_at_the_top_left_of_the_screen_is_functional_and_takes_players_back_to_leaderboard_screen(Common):
    """
    TR_ID: C64368258
    NAME: Verify the back button at the top left of the screen is functional and takes players back to leaderboard screen
    DESCRIPTION: This Testcase verifies the functionality for back button in the  leaderboard
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_edp_page_for_which_leaderboard_is_available(self):
        """
        DESCRIPTION: Navigate to Golf EDP page for which Leaderboard is available.
        EXPECTED: User should be able to tap on player name in the board.
        """
        pass

    def test_002_click_on_any_player_name_from_scoreboard(self):
        """
        DESCRIPTION: Click on any player name from scoreboard.
        EXPECTED: Clicking on player name should redirect to current active course map.
        """
        pass

    def test_003_click_on_back_button_which_is_available_at_top_left_of_the_screen(self):
        """
        DESCRIPTION: Click on back button which is available at top left of the screen.
        EXPECTED: Clicking on back button user should be naviage back to main leaderboard screen
        """
        pass
