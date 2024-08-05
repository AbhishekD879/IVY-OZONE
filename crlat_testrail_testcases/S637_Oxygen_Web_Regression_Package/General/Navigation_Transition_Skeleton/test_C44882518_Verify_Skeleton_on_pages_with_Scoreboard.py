import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44882518_Verify_Skeleton_on_pages_with_Scoreboard(Common):
    """
    TR_ID: C44882518
    NAME: Verify Skeleton on pages with Scoreboard
    DESCRIPTION: This test case verifies loading skeleton for pages with Scoreboard components so that user get feedback that something is happening when opening a page.
    PRECONDITIONS: - Skeleton feature is turned on in CMS (System Cofig-> Structure-> Feature Toggle: 'skeletonLoadingScreen')
    PRECONDITIONS: - Should be created an event with Scoreboard.
    PRECONDITIONS: Scoreboards shown on:
    PRECONDITIONS: Sport EDP's
    """
    keep_browser_open = True

    def test_001_launch_the_app_and_open_edp_page_with_scoreboard(self):
        """
        DESCRIPTION: Launch the app and open EDP page with Scoreboard.
        EXPECTED: User should be able to see a loading full skeleton page instead of missing content.
        EXPECTED: When all content became available (except Scoreboard) user will see the Scoreboard loading skeleton.
        EXPECTED: ![](index.php?/attachments/get/53285764)
        EXPECTED: ![](index.php?/attachments/get/53285763)
        """
        pass

    def test_002_check_the_skeleton_animation_while_page_skeleton_is_displayed_to_the_user(self):
        """
        DESCRIPTION: Check the skeleton animation while page skeleton is displayed to the user
        EXPECTED: User sees shimmering animation when viewing loading skeletons
        """
        pass

    def test_003_verify_the_page_transition_when_content_becomes_available(self):
        """
        DESCRIPTION: Verify the page transition when content becomes available
        EXPECTED: When content becomes available on the page user sees a smooth transition from the loading skeleton to the full page content
        """
        pass

    def test_004_repeat_steps_1_3_with_other_types_of_scoreboard_list_of_the_pages_in_precondition(self):
        """
        DESCRIPTION: Repeat steps 1-3 with other types of Scoreboard (list of the pages in precondition)
        EXPECTED: 
        """
        pass
