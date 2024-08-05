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
class Test_C64663366_Verify_the_Player_selection_details_of_Score_cast_market_template(Common):
    """
    TR_ID: C64663366
    NAME: Verify the Player selection details of Score cast market template
    DESCRIPTION: This test case Verifies the display Scorecast market template
    PRECONDITIONS: Scorecast template should be configured/mapped to the event
    PRECONDITIONS: This will be a 2-phase selection template, with the first phase leading on to the second phase based on selection:
    PRECONDITIONS: Phase 1: Player Selection
    PRECONDITIONS: ![](index.php?/attachments/get/00e318db-8d31-44db-93d5-64df950cb396)
    PRECONDITIONS: Phase 2: Scoreline Selection
    PRECONDITIONS: ![](index.php?/attachments/get/124c7123-e3ad-4a04-a067-5ef4f66ae905)
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
        EXPECTED: * Market Header (including signposting if applied)
        EXPECTED: * ---2.Market Blurb (if applied)---OutofScope for NOW
        EXPECTED: * List of Player Name Links
        EXPECTED: * “SHOW MORE/“SHOW LESS…” Link should be available [when selects  show more remaining selections  should be revealed to the user and "SHOW MORE..." link should be replaced with a "SHOW LESS..." Link]
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/0d43e572-4ec1-48fc-a7ab-9a847ce84d46)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/12b7009f-8d01-401f-adc4-b2fcfffb3c0e)
        """
        pass

    def test_004_validate_user_is_able_to_see_a_list_of_player_name_for_scorecast_market(self):
        """
        DESCRIPTION: Validate user is able to see a list of player name for scorecast market
        EXPECTED: * Player should be slected and Scoreline Selection pop-up appers
        """
        pass

    def test_005_validate_scoreline_selection_pop_up_screen_after_player_selection(self):
        """
        DESCRIPTION: Validate Scoreline Selection pop-up screen after player selection
        EXPECTED: * Market Title
        EXPECTED: * Close (X) Button
        EXPECTED: * Player Selected & Blurb Text reading(outof scope for now)
        EXPECTED: * List of Pre-defined "Home Team Victory" Price Buttons
        EXPECTED: * List of Pre-defined "Draw" Price Buttons (with Labels)
        EXPECTED: * List of Pre-defined "Away Team Victory" Price Buttons (with Labels)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/7b3fe772-3a76-462c-811a-806fda349ff2)
        """
        pass

    def test_006_after_selection_the_scoreline_selection_click_on_x_close_button(self):
        """
        DESCRIPTION: After selection the scoreline selection click on (X) Close button
        EXPECTED: * Scoreline Selection pop-up will closed and back to the player selection screen
        """
        pass
