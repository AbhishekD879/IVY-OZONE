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
class Test_C64293334_verify_user_is_allowed_to_navigate_back_to_groups_tab_by_clicking_back_button(Common):
    """
    TR_ID: C64293334
    NAME: verify user is allowed to navigate back to groups tab by clicking back button
    DESCRIPTION: This tc verifies the functionality of Back button in follow a hole screen
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. Open follow a hole screen by clicking on any of the hole images from Course tab
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

    def test_005_tap_on_back_button_on_follow_a_hole_screen(self):
        """
        DESCRIPTION: Tap on back button on follow a hole screen
        EXPECTED: User should be redirected back to Course tab.
        """
        pass
