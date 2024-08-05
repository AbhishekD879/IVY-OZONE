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
class Test_C64293338_validation_of_noof_holes_in_course_tab(Common):
    """
    TR_ID: C64293338
    NAME: validation of no.of holes in course tab
    DESCRIPTION: This tc validates the no. of holes displayed on FE and the backend data
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User logged in.
    PRECONDITIONS: 5. Navigate to GOLF inplay event with IMG LB
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

    def test_004_open_network_tab_and_verify_the_img_data_related_holes(self):
        """
        DESCRIPTION: Open network tab and verify the IMG data related holes.
        EXPECTED: Data sent by IMG should be displayed correctly
        """
        pass
