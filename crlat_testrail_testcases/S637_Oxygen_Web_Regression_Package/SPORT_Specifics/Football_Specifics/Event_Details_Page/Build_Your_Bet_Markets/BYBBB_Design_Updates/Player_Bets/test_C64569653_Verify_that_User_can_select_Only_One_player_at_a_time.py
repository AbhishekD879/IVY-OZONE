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
class Test_C64569653_Verify_that_User_can_select_Only_One_player_at_a_time(Common):
    """
    TR_ID: C64569653
    NAME: Verify that User can select Only One player at a time
    DESCRIPTION: Verify that User can select Only One player at a time
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

    def test_004_validate_the_display_of_player_bets(self):
        """
        DESCRIPTION: Validate the display of Player Bets
        EXPECTED: * Player Bets should no longer be displayed in dropdown view
        EXPECTED: * Player Bets should be displayed in their own accordions
        EXPECTED: * Player Total Assists
        EXPECTED: * Player Total Passes
        EXPECTED: * Player Total Shots
        EXPECTED: * Player Total Shots on Target
        EXPECTED: * Player Total Tackles
        EXPECTED: * Player Shots Outside the box
        EXPECTED: * Offside
        EXPECTED: * Player Total Goals
        EXPECTED: * Goals Inside the box
        EXPECTED: * Goals Outside the box
        """
        pass

    def test_005_expand_any_player_market_mentioned_in_the_above_step_and_validate_the_display_of_player_names(self):
        """
        DESCRIPTION: Expand any Player Market mentioned in the above step and Validate the display of Player names
        EXPECTED: * Market should be expanded
        EXPECTED: * Select Team should be displayed with three filters - Both Teams, Team A , Team B
        EXPECTED: * By default Both Team should be selected
        EXPECTED: * Player Names should be displayed in List view
        EXPECTED: * Crest/Flag should be displayed before the player name - Asset Manager CMS
        EXPECTED: * Player position should be displayed beside Player Name
        EXPECTED: * Stats related to the Market should be displayed for that Player
        EXPECTED: Example if its Player Total Passes Market - Passes stats for the player should be displayed
        EXPECTED: * Show Stats Link should be displayed
        """
        pass

    def test_006_validate_the_filters_both_teams_team_a__team_b(self):
        """
        DESCRIPTION: Validate the Filters Both Teams, Team A , Team B
        EXPECTED: **Both Teams**
        EXPECTED: * Players from Both Teams should be displayed
        EXPECTED: **Team A**
        EXPECTED: * Players from only Team A (Home) should be displayed
        EXPECTED: **Team B**
        EXPECTED: * Players from only Team B (Away) should be displayed
        """
        pass

    def test_007_expand_the_player_name_by_clicking_on_the_chevron(self):
        """
        DESCRIPTION: Expand the Player name by clicking on the chevron
        EXPECTED: * Player Name should be Expanded
        EXPECTED: * Stats Increment should be displayed
        EXPECTED: * Increments of 1 should be displayed
        EXPECTED: * ADD TO BET BUILDER/ ADD TO BETSLIP CTA should be displayed
        """
        pass

    def test_008_for_the_player_markets___validate_only_one_player_can_be_selected_at_a_time(self):
        """
        DESCRIPTION: For the Player Markets - Validate Only one Player can be selected at a Time
        EXPECTED: Only One player at a time should be selected
        """
        pass
