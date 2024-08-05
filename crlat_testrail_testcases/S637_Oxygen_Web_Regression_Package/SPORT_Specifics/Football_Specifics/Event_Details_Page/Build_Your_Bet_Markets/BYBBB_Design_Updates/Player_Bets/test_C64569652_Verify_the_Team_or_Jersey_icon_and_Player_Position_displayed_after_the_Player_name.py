import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569652_Verify_the_Team_or_Jersey_icon_and_Player_Position_displayed_after_the_Player_name(Common):
    """
    TR_ID: C64569652
    NAME: Verify the Team or Jersey icon and Player Position displayed after the Player name
    DESCRIPTION: Test case verifies Player Position displayed after the Player name
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB tab should be displayed with all the Markets
        """
        pass

    def test_004_expand_any_player_market_mentioned_in_the_above_step_and_validate_the_display_of_player_names(self):
        """
        DESCRIPTION: Expand any Player Market mentioned in the above step and Validate the display of Player names
        EXPECTED: * Team/ Jersey and Player position should be displayed beside Player Name
        EXPECTED: * Stats related to the Market should be displayed for that Player
        EXPECTED: Example if its Player Total Passes Market - Passes stats for the player should be displayed
        EXPECTED: * Show Stats Link should be displayed
        """
        pass

    def test_005_validate_player_position_is_displayed_beside_player_name_for_all_both_teams_team_a__team_b_players(self):
        """
        DESCRIPTION: Validate player position is displayed beside player name for all Both Teams, Team A , Team B players
        EXPECTED: **Both Teams**
        EXPECTED: * Player position should be displayed beside Player Name
        EXPECTED: **Team A**
        EXPECTED: * Player position should be displayed beside Player Name
        EXPECTED: **Team B**
        EXPECTED: * Player position should be displayed beside Player Name
        """
        pass

    def test_006_click_on_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * User should be able to click and selection should be added BYB/BB betslip
        EXPECTED: * ADDED should be displayed
        """
        pass
