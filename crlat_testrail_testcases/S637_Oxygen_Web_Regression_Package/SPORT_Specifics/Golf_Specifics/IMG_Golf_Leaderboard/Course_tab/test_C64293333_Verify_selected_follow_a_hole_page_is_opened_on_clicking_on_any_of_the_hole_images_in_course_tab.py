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
class Test_C64293333_Verify_selected_follow_a_hole_page_is_opened_on_clicking_on_any_of_the_hole_images_in_course_tab(Common):
    """
    TR_ID: C64293333
    NAME: Verify selected follow a hole page is opened on clicking on any of the hole images in course tab
    DESCRIPTION: This tc verifies the functionality of hole icon on Course screen
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
        EXPECTED: Course tab is opened.
        """
        pass

    def test_004_click_on_any_of_the_images_from_the_available_holes_list_to_open_follow_a_hole_screen(self):
        """
        DESCRIPTION: Click on any of the images from the available holes list to open follow a hole screen.
        EXPECTED: Follow a hole screen should be displayed on tapping any of the hole images.
        """
        pass
