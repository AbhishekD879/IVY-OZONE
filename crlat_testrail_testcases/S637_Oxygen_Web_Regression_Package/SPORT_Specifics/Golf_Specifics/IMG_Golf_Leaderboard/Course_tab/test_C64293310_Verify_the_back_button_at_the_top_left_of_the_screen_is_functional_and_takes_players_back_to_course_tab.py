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
class Test_C64293310_Verify_the_back_button_at_the_top_left_of_the_screen_is_functional_and_takes_players_back_to_course_tab(Common):
    """
    TR_ID: C64293310
    NAME: Verify the back button at the top left of the screen is functional and takes players back to course tab
    DESCRIPTION: This Testcase verifies the functionality for back button in the hole streaming page.
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS&gt; System Configuration &gt; Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. Course tab should have active streaming for atleast 1 hole.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_edp_page_for_which_leaderboard_is_available(self):
        """
        DESCRIPTION: Navigate to Golf EDP page for which Leaderboard is available.
        EXPECTED: Leaderboard is displayed
        """
        pass

    def test_002_tapclick_on_course_tab(self):
        """
        DESCRIPTION: Tap/click on Course tab
        EXPECTED: Course tab should be opened.
        """
        pass

    def test_003_tap_on_play_button_below_the_hole_image(self):
        """
        DESCRIPTION: Tap on play button below the hole image.
        EXPECTED: Streaming is opened.
        """
        pass

    def test_004_clicktap_on_back_button_at_the_top_left_of_the_screen(self):
        """
        DESCRIPTION: Click/Tap on Back button at the top left of the screen.
        EXPECTED: Player is redirected back to course tab.
        """
        pass
