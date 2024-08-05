import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64663372_Verify_User_is_navigating_back_to_Player_selection_screen_after_closing_Score_line_popup(Common):
    """
    TR_ID: C64663372
    NAME: Verify User is navigating back to Player selection screen after closing Score line popup
    DESCRIPTION: This test case verifies navigating back to player selection screen after selecting scoreline
    PRECONDITIONS: Scorecast template should be configured/mapped to the event
    PRECONDITIONS: This will be a 2-phase selection template, with the first phase leading on to the second phase based on selection:
    PRECONDITIONS: Phase 1: Player Selection
    PRECONDITIONS: ![](index.php?/attachments/get/9dc1fba8-e8cc-47db-b5e5-2981890fe482)
    PRECONDITIONS: Phase 2: Scoreline Selection
    PRECONDITIONS: ![](index.php?/attachments/get/0655f414-e74b-4bfa-884e-ccce0acbe8a6)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_any_sports__edp_page(self):
        """
        DESCRIPTION: Navigate to any sports  EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_the_markets_which_should_display_the_score_cast_template(self):
        """
        DESCRIPTION: Expand the markets which should display the Score cast Template
        EXPECTED: 1.Market Header (including signposting if applied)
        EXPECTED: --------------2.Market Blurb (if applied)---OutOF Scpe for NOW
        EXPECTED: 3.List of Player Name Links
        EXPECTED: 4.Show More Link
        EXPECTED: 5.Show Less link
        """
        pass

    def test_004_click_on_any_player_name_link(self):
        """
        DESCRIPTION: Click on any player name link
        EXPECTED: Player should be slected and Scoreline Selection pop-up appers
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/3b8d72b0-a726-443d-aa83-271f4b3cb7f1)
        """
        pass

    def test_005_click_on_close_x_button(self):
        """
        DESCRIPTION: Click on Close X button
        EXPECTED: Pop Up should be closed and User should be navigated back to Score cast template page
        """
        pass
