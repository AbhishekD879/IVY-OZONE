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
class Test_C64293305_Verify_the_map_view_changes_accordingly_when_we_change_view_from_2d_to_3d_and_viceversa(Common):
    """
    TR_ID: C64293305
    NAME: Verify the map view changes accordingly when we change view from 2d to 3d and viceversa
    DESCRIPTION: This Testcase verifies map viewwhen the 2d/3d toggle is selected in the  leaderboard
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

    def test_003_change_the_toggle_to_2d_and_3d_and_verify_the_map_changes_accordingly(self):
        """
        DESCRIPTION: Change the toggle to 2D and 3D and verify the map changes accordingly.
        EXPECTED: Map view should be changed based on toggle selection
        """
        pass
