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
class Test_C64293304_Verify_a_toggle_to_switch_between_2d_3d_views_are_available(Common):
    """
    TR_ID: C64293304
    NAME: Verify a toggle to switch between 2d & 3d views are available
    DESCRIPTION: This Testcase verifies functionality of 2d/3d toggle in the  leaderboard
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_in_play_event_edp_page(self):
        """
        DESCRIPTION: Navigate to golf in-play event EDP page
        EXPECTED: User should be navigated to Leaderboard when the event is in-play
        """
        pass

    def test_002_verify_the_leader_board_is_displayed_in_golf_edp_page(self):
        """
        DESCRIPTION: Verify the Leader board is displayed in golf EDP page.
        EXPECTED: User should be displayed Leaderboard
        """
        pass

    def test_003_click_on_any_player_name_from_scoreboard(self):
        """
        DESCRIPTION: Click on any player name from scoreboard.
        EXPECTED: User should be able to tap on player name in the board and Clicking on player name should redirect to current active course map.
        """
        pass

    def test_004_verify_the_functionality_of_2d3d_toggle(self):
        """
        DESCRIPTION: Verify the functionality of 2D/3D toggle
        EXPECTED: User should be able to switch between 2d and 3d view.
        """
        pass
