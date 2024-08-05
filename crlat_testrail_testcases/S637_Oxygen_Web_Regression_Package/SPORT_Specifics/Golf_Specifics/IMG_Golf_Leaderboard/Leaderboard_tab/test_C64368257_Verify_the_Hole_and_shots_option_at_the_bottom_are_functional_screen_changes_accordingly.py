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
class Test_C64368257_Verify_the_Hole_and_shots_option_at_the_bottom_are_functional_screen_changes_accordingly(Common):
    """
    TR_ID: C64368257
    NAME: Verify the Hole and shots option at the bottom are functional & screen changes accordingly
    DESCRIPTION: This Testcase verifies the functionality for Hole and shots option at the bottom in the  leaderboard
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

    def test_003_verify_holescoreboard_shots_options_are_available_at_the_bottom_of_the_page(self):
        """
        DESCRIPTION: verify hole,scoreboard, shots options are available at the bottom of the page.
        EXPECTED: hole,scoreboard, shots options should be available at the bottom of the page.
        """
        pass

    def test_004_click_on_each_option_and_verify_its_redirected_to_respective_page(self):
        """
        DESCRIPTION: Click on each option and verify its redirected to respective page.
        EXPECTED: Clicking on each option should be redirected tocorrect page and diaplyed data should be correct.
        """
        pass
