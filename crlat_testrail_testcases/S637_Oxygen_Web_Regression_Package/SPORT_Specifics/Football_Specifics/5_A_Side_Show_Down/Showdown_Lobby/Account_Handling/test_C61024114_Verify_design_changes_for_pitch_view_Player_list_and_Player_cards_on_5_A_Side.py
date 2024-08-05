import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C61024114_Verify_design_changes_for_pitch_view_Player_list_and_Player_cards_on_5_A_Side(Common):
    """
    TR_ID: C61024114
    NAME: Verify design changes for pitch view, Player list and Player cards on 5-A-Side
    DESCRIPTION: This testcase verifies the colour of pitch view in 5-A-Side
    PRECONDITIONS: Applicable only for Ladbrokes.
    PRECONDITIONS: 5-A-Side should be enabled in CMS.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes(self):
        """
        DESCRIPTION: Launch Ladbrokes
        EXPECTED: User should be able to access Ladbrokes application
        """
        pass

    def test_002_navigate_to_5_a_side_tab(self):
        """
        DESCRIPTION: Navigate to 5-A-Side Tab
        EXPECTED: User should be navigated to the 5-A-side.
        """
        pass

    def test_003_click_on_any_of_the_available_5_a_side_matches(self):
        """
        DESCRIPTION: Click on any of the available 5-A-Side matches
        EXPECTED: User should be navigated to 5-A-Side Match
        """
        pass

    def test_004_click_on_build_a_team(self):
        """
        DESCRIPTION: Click on 'Build A Team'
        EXPECTED: User is navigated to the pitch view
        """
        pass

    def test_005_verify_the_colour_of_the_pitch_view(self):
        """
        DESCRIPTION: Verify the colour of the pitch view
        EXPECTED: The pitch view should be in darker mode
        """
        pass

    def test_006_click_on_the_plus_symbol_on_the_pitch_view_to_add_the_players(self):
        """
        DESCRIPTION: Click on the '+' symbol on the pitch view to add the players
        EXPECTED: User should be navigated to the player list. The Player list background should be in dark mode.
        """
        pass

    def test_007_click_on_a_player_from_the_player_list(self):
        """
        DESCRIPTION: Click on a player from the player list
        EXPECTED: User will be navigated to the player card of the respective player.
        EXPECTED: The player card should be in dark mode.
        """
        pass
