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
class Test_C64293332_Verify_the_hole_number_and_players_count_is_displayes_below_the_hole_image(Common):
    """
    TR_ID: C64293332
    NAME: Verify the hole number and players count is displayes below the hole image
    DESCRIPTION: This tc validates the hole number & player count displayed below the hole image
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application.
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_leaderboard_when_the_event_is_inplay(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is inplay.
        EXPECTED: LB should load
        """
        pass

    def test_003_navigate_to_course_tab(self):
        """
        DESCRIPTION: Navigate to Course tab.
        EXPECTED: Course tab is opened. Hole number & player count should be displayed below the hole image
        """
        pass