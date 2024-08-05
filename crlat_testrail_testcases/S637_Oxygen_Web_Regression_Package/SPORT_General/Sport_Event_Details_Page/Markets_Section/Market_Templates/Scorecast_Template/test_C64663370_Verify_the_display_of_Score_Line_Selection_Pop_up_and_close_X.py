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
class Test_C64663370_Verify_the_display_of_Score_Line_Selection_Pop_up_and_close_X(Common):
    """
    TR_ID: C64663370
    NAME: Verify the display of Score Line Selection Pop-up and close X
    DESCRIPTION: Verify the Score cast template
    PRECONDITIONS: Scorecast template should be configured/mapped to the event
    PRECONDITIONS: This will be a 2-phase selection template, with the first phase leading on to the second phase based on selection:
    PRECONDITIONS: Phase 1: Player Selection
    PRECONDITIONS: Phase 2: Scoreline Selection
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
        EXPECTED: 2.List of Player Name Links
        EXPECTED: 3.Show More Link
        EXPECTED: 4.Show Less link
        """
        pass

    def test_004_click_on_any_player_name_link(self):
        """
        DESCRIPTION: Click on Any player name link
        EXPECTED: Page should be navigated to Scoreline Selection pop-up
        """
        pass

    def test_005_validate_scoreline_popup_content(self):
        """
        DESCRIPTION: Validate Scoreline popup content
        EXPECTED: 1.Market Title
        EXPECTED: 2.Close (X) Button
        EXPECTED: 3.Player Selected & Blurb Text reading(outof scope for now)
        EXPECTED: 4.List of Pre-defined "Home Team Victory" Price Buttons
        EXPECTED: 5.List of Pre-defined "Draw" Price Buttons (with Labels)
        EXPECTED: 6.List of Pre-defined "Away Team Victory" Price Buttons (with Labels)
        EXPECTED: ![](index.php?/attachments/get/dddc3da8-25d6-4e94-9c68-3074fe1c4d5e)
        """
        pass

    def test_006_click_on_outside_of_scoreline_popup_and_check_pop_up_is_getting_removed(self):
        """
        DESCRIPTION: Click on Outside of Scoreline popup and check pop up is getting removed
        EXPECTED: Scoreline popup should NOT be removed
        """
        pass

    def test_007_after_selection_the_scoreline_selection_click_on_x_close_button(self):
        """
        DESCRIPTION: After selection the scoreline selection click on (X) Close button
        EXPECTED: Scoreline Selection pop-up will closed and back to the player selection screen
        """
        pass
