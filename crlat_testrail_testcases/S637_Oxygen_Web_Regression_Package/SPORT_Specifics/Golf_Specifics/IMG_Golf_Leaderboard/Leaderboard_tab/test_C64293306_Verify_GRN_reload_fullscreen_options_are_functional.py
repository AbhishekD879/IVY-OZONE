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
class Test_C64293306_Verify_GRN_reload_fullscreen_options_are_functional(Common):
    """
    TR_ID: C64293306
    NAME: Verify GRN, reload & fullscreen options are functional
    DESCRIPTION: This Testcase verifies the functionality for GRN, reload & fullscreen options in the  leaderboard
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

    def test_003_verify_grnreloadfullscreen_options_available_at_the_right_top_corner(self):
        """
        DESCRIPTION: Verify GRN,Reload,Fullscreen options available at the right top corner.
        EXPECTED: GRN,Reload,Fullscreen options should be available at the right top corner.
        """
        pass

    def test_004_verify_the_functionality_is_working_as_expected(self):
        """
        DESCRIPTION: Verify the functionality is working as expected.
        EXPECTED: Clicking on:
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: 1) GRN - Green area should display.
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2) Reload - Reload the map to previous position
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: 3) Fullscreen - Map should display in full screen size.
        """
        pass
