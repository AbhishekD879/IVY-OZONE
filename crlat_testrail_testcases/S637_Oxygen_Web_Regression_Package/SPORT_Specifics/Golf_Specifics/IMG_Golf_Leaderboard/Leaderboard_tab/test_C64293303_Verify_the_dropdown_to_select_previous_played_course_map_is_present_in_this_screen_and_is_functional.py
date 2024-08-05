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
class Test_C64293303_Verify_the_dropdown_to_select_previous_played_course_map_is_present_in_this_screen_and_is_functional(Common):
    """
    TR_ID: C64293303
    NAME: Verify the dropdown to select previous played course map is present in this screen and is functional
    DESCRIPTION: This Testcase verifies functionality of dropdown to select the map of previous players in the  leaderboard
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
        EXPECTED: User should be able to tap on player name in the board.
        """
        pass

    def test_004_verify_the_options_from_dropdown_are_clickable_and_also_verify_the_player_information_diaplyed_accordingly(self):
        """
        DESCRIPTION: Verify the options from dropdown are clickable and also verify the player information diaplyed accordingly.
        EXPECTED: User should be able to select the options from dropdown and Clicking on player name user should redirect to current active course map.
        """
        pass
