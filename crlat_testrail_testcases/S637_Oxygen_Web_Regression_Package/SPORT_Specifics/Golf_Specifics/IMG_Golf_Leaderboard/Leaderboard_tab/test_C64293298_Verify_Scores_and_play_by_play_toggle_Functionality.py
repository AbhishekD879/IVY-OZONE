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
class Test_C64293298_Verify_Scores_and_play_by_play_toggle_Functionality(Common):
    """
    TR_ID: C64293298
    NAME: Verify Scores and play by play toggle Functionality
    DESCRIPTION: This Testcase verifies the Scores and play by play toggle functionality in the header of Leaderboard tab
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
        DESCRIPTION: Verify the Leader board is displayed in golf EDP page
        EXPECTED: User should be displayed Leaderboard
        """
        pass

    def test_003_verify_scores_toggle_is_selected_by_default(self):
        """
        DESCRIPTION: Verify Scores toggle is selected by default.
        EXPECTED: User should see scores toggle is selected by default.
        """
        pass

    def test_004_verify_the_view_of_leaderboard_when_the_score_toggle_is_selected(self):
        """
        DESCRIPTION: Verify the view of leaderboard when the score toggle is selected
        EXPECTED: User should see score view in the leaderboard.
        """
        pass

    def test_005_verify_the_view_of_leaderboard_when_the_play_by_play_toggle_is_selected(self):
        """
        DESCRIPTION: Verify the view of leaderboard when the play by play toggle is selected
        EXPECTED: User should see play by play view in the leaderboard.
        """
        pass

    def test_006_select_play_by_play_toggleredirect_to_any_other_page_and_come_back_again(self):
        """
        DESCRIPTION: Select play by play toggle,redirect to any other page and come back again
        EXPECTED: User should see scores toggle is selected by default.
        """
        pass
