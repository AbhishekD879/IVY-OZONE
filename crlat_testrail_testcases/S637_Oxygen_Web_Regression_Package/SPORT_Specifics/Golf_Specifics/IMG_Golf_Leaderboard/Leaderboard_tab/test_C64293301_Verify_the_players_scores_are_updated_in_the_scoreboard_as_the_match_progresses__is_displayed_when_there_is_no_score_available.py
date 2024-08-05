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
class Test_C64293301_Verify_the_players_scores_are_updated_in_the_scoreboard_as_the_match_progresses__is_displayed_when_there_is_no_score_available(Common):
    """
    TR_ID: C64293301
    NAME: Verify the players scores are updated in the scoreboard as the match progresses & '-' is displayed when there is no score available
    DESCRIPTION: This Testcase verifies thescores data displayed in the leaderboard
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

    def test_003_verify_the_scores_in_the_scoreboard_are_updated_and_highlighting_when_the_match_is_in_progress(self):
        """
        DESCRIPTION: Verify the scores in the scoreboard are updated and highlighting when the match is in progress.
        EXPECTED: players scores should be updated in the scoreboard as the match in progress
        """
        pass

    def test_004_also_verify_the_the_behaviour_when_there_is_no_score_available(self):
        """
        DESCRIPTION: Also verify the the behaviour when there is no score available.
        EXPECTED: '-' should be displayed when there is no score available
        """
        pass
