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
class Test_C64293300_Verify_the_playoff_name_is_displayed_1st_followed_by_a_table_with_playoff_num_hole_count_par_and_then_players_score(Common):
    """
    TR_ID: C64293300
    NAME: Verify the playoff name is displayed 1st, followed by a table with playoff num, hole count, par and then players score
    DESCRIPTION: This Testcase verifies the data displayed in the leaderboard
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_in_play_event_edp_page(self):
        """
        DESCRIPTION: Navigate to golf in-play event EDP page
        EXPECTED: 1. User should be navigated to Leaderboard when the event is in-play
        """
        pass

    def test_002_verify_the_leader_board_is_displayed_in_golf_edp_page(self):
        """
        DESCRIPTION: Verify the Leader board is displayed in golf EDP page.
        EXPECTED: 2. User should be displayed Leaderboard
        """
        pass

    def test_003_verify_the_left_view_columns_of_the_leaderboardalso_verify_the_player_score_table_view_and_data_displayed(self):
        """
        DESCRIPTION: Verify the left view columns of the leaderboard,Also verify the player score table view and data displayed.
        EXPECTED: 3.playoff name should be displayed 1st, followed by a table with playoff num, hole count, par and then players score
        """
        pass
