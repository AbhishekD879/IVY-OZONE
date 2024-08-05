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
class Test_C64293359_Verify_the_display_of_Play_icon_in_course_tab_when_streaming_is_available(Common):
    """
    TR_ID: C64293359
    NAME: Verify the display of Play icon in course tab when  streaming is available
    DESCRIPTION: This tc verifies the display of play icon in course tab.
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS&gt; System Configuration &gt; Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3.Inplay event should be mapped with IMG feed provider event Id.
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

    def test_004_play_icon_should_be_displayed_in_the_following_places_when_streaming_is_available_1_on_course_tab2_below_the_hole_images_for_which_the_streaming_is_available(self):
        """
        DESCRIPTION: Play icon should be displayed in the following places when streaming is available :
        DESCRIPTION: 1. On course tab,
        DESCRIPTION: 2. Below the hole images for which the streaming is available
        EXPECTED: Play icon should be displayed in mentioned places when streaming is available.
        """
        pass

    def test_005_play_icon_should_not_be_displayed_for_holes_which_does_not_have_streaming(self):
        """
        DESCRIPTION: Play icon should not be displayed for holes which does not have streaming
        EXPECTED: Play icon should not be displayed for holes which does not have streaming
        """
        pass
