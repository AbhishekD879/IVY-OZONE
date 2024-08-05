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
class Test_C64293331_Verify_if_images_of_all_holes_are_displayed_in_course_tab_and_are_clickable(Common):
    """
    TR_ID: C64293331
    NAME: Verify if images of all holes are displayed in course tab and are clickable
    DESCRIPTION: This tc verifies the functionality of Holes images displayed in course tab.
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
        EXPECTED: Course tab is opened
        """
        pass

    def test_004_tap_on_any_of_the_hole_icon_from_available_holes_list(self):
        """
        DESCRIPTION: Tap on any of the hole icon from available holes list.
        EXPECTED: Follow a hole screen is loaded
        """
        pass
