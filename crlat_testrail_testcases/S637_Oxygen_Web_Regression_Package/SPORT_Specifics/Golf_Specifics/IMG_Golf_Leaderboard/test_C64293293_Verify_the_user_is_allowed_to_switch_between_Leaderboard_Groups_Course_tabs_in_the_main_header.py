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
class Test_C64293293_Verify_the_user_is_allowed_to_switch_between_Leaderboard_Groups_Course_tabs_in_the_main_header(Common):
    """
    TR_ID: C64293293
    NAME: Verify the user is allowed to switch between Leaderboard, Groups & Course tabs in the main header.
    DESCRIPTION: This Testcase verifies whether user is allowed to switch between Leaderboard, Groups & Course tabs in the main header.
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

    def test_003_verify_that_switching_between_the_tabs_is_working_fine(self):
        """
        DESCRIPTION: Verify that switching between the tabs is working fine
        EXPECTED: User should be able to switch between all the 3 tabs.
        """
        pass
