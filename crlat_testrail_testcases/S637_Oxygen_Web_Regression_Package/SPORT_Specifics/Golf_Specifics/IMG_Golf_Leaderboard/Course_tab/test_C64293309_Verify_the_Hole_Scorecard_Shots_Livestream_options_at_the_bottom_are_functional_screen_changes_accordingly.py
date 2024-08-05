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
class Test_C64293309_Verify_the_Hole_Scorecard_Shots_Livestream_options_at_the_bottom_are_functional_screen_changes_accordingly(Common):
    """
    TR_ID: C64293309
    NAME: Verify the Hole, Scorecard, Shots & Livestream options at the bottom are functional & screen changes accordingly
    DESCRIPTION: This Testcase verifies the functionality for Hole, Scorecard, shots & Livestream options at the bottom in the hole streaming screen.
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS&gt; System Configuration &gt; Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. Course tab in LB should have active streaming atleast for 1 hole.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_edp_page_for_which_leaderboard_is_available(self):
        """
        DESCRIPTION: Navigate to Golf EDP page for which Leaderboard is available.
        EXPECTED: Leaderboard is opened.
        """
        pass

    def test_002_click_on_course_tab(self):
        """
        DESCRIPTION: Click on Course tab.
        EXPECTED: Course tab should be opened.
        """
        pass

    def test_003_tapclick_on_play_button_displayed_below_hole_image(self):
        """
        DESCRIPTION: Tap/Click on Play button displayed below hole image.
        EXPECTED: Streaming is opened.
        """
        pass

    def test_004_verify_hole_scoreboard_shots__livestream_options_are_available_at_the_bottom_of_the_page(self):
        """
        DESCRIPTION: verify hole, scoreboard, shots & Livestream options are available at the bottom of the page.
        EXPECTED: hole, scoreboard, shots & Livestream options should be available at the bottom of the page.
        """
        pass

    def test_005_click_on_each_option_and_verify_its_redirected_to_respective_page(self):
        """
        DESCRIPTION: Click on each option and verify its redirected to respective page.
        EXPECTED: Clicking on each option should be redirected to correct page and displayed data should be correct.
        """
        pass
