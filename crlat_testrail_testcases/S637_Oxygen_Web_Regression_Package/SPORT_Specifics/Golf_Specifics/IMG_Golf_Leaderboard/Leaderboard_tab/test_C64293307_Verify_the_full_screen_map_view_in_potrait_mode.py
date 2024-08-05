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
class Test_C64293307_Verify_the_full_screen_map_view_in_potrait_mode(Common):
    """
    TR_ID: C64293307
    NAME: Verify the full screen map view in potrait mode
    DESCRIPTION: This testcase verifies the map in full screen
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. Application is opened in potrait mode
    """
    keep_browser_open = True

    def test_001_open_application_in_potrait_mode(self):
        """
        DESCRIPTION: Open application in potrait mode.
        EXPECTED: User should see the appliation in potrait mode
        """
        pass

    def test_002_navigate_to_golf_edp_page_for_which_leaderboard_is_available(self):
        """
        DESCRIPTION: Navigate to Golf EDP page for which Leaderboard is available.
        EXPECTED: User should navigate to EDP page
        """
        pass

    def test_003_tap_on_any_player_name_from_scoreboard(self):
        """
        DESCRIPTION: Tap on any player name from scoreboard.
        EXPECTED: User should be able to tap on playername.
        """
        pass

    def test_004_tap_on_map_full_screen_button(self):
        """
        DESCRIPTION: Tap on map full screen button.
        EXPECTED: Full screen map view opens in potrait mode
        """
        pass
