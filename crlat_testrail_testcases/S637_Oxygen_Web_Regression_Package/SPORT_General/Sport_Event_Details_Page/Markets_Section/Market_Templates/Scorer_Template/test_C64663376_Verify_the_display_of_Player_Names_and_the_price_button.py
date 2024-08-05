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
class Test_C64663376_Verify_the_display_of_Player_Names_and_the_price_button(Common):
    """
    TR_ID: C64663376
    NAME: Verify the display of Player Names and the price button
    DESCRIPTION: This test case verifies the display of players name for scorer markets
    PRECONDITIONS: 1.Market which fall under scorer format should follow this templet
    PRECONDITIONS: ![](index.php?/attachments/get/443fd39e-eb11-43d5-bdb6-1720c493b320)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: * User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_sports__edp_page(self):
        """
        DESCRIPTION: Navigate to sports  EDP page
        EXPECTED: * EDP page should be displayed
        """
        pass

    def test_003_expand_the_markets_which_should_display_the_scorer_template(self):
        """
        DESCRIPTION: Expand the markets which should display the Scorer Template
        EXPECTED: * Market Header should be displayed for scorer templet available
        EXPECTED: * "PLAYERS" Label
        EXPECTED: * List of Options (each with Player Name, Team Name & Price Button)
        """
        pass

    def test_004_validate_the_player_name_an_the_price_button__for_the_scorer_markets(self):
        """
        DESCRIPTION: Validate the player name an the price button  for the scorer markets
        EXPECTED: Player Name and price button  should be displayed for scorer market
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/84da1490-bebb-49e8-b08e-c97cb4fc3a36)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/7a2a9e1e-f5c4-4a79-8db4-c7e6f1424d34)
        """
        pass
