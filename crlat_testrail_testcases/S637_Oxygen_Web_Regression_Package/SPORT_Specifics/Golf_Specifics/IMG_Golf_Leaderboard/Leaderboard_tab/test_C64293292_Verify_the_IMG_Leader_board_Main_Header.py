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
class Test_C64293292_Verify_the_IMG_Leader_board_Main_Header(Common):
    """
    TR_ID: C64293292
    NAME: Verify the IMG Leader board Main Header
    DESCRIPTION: This Testcase verifies the IMG Leaderboard Header content.
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

    def test_003_verify_the_header_tabs_in_img_leaderboard(self):
        """
        DESCRIPTION: Verify the header tabs in IMG LeaderBoard
        EXPECTED: User should be displayed with the below tabs:
        EXPECTED: LeaderBoard
        EXPECTED: Groups
        EXPECTED: Course
        """
        pass
