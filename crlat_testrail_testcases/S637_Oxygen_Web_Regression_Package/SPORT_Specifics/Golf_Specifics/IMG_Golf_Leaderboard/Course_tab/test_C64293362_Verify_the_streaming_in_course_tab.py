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
class Test_C64293362_Verify_the_streaming_in_course_tab(Common):
    """
    TR_ID: C64293362
    NAME: Verify the streaming in course tab
    DESCRIPTION: This tc verifies the streaming in Follow a hole screen of course tab.
    PRECONDITIONS: "1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS&gt; System Configuration &gt; Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User logged in.
    PRECONDITIONS: 5. Navigate to GOLF inplay event with IMG LB.
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
        EXPECTED: Course tab is opened.
        """
        pass

    def test_004_click_on_play_icon_displayed_below_hole_image(self):
        """
        DESCRIPTION: Click on Play icon displayed below hole image.
        EXPECTED: streaming should be displayed.
        """
        pass
