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
class Test_C64293335_Verify_GRN_reload_fullscreen_options_are_functional(Common):
    """
    TR_ID: C64293335
    NAME: Verify GRN, reload & fullscreen options are functional
    DESCRIPTION: This tc verifies the functionality of GRN, Reload & full screen options on Follow a hole screen
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

    def test_005_verify_grnreloadfullscreen_options_available_at_the_right_top_corner(self):
        """
        DESCRIPTION: Verify GRN,Reload,Fullscreen options available at the right top corner.
        EXPECTED: GRN,Reload,Fullscreen options should be available at the right top corner & are functional
        """
        pass

    def test_006_verify_the_functionality_is_working_as_expected(self):
        """
        DESCRIPTION: Verify the functionality is working as expected.
        EXPECTED: 1) GRN - Zoom the map.
        """
        pass

    def test_007_(self):
        """
        DESCRIPTION: 
        EXPECTED: 2) Reload - Reload the map to previous position
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: 3) Fullscreen - Map should display in full screen size.
        """
        pass
