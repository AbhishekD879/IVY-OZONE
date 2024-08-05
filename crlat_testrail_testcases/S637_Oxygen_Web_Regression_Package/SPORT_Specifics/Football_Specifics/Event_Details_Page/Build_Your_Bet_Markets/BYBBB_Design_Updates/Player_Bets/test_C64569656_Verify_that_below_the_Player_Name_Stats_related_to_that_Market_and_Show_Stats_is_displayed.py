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
class Test_C64569656_Verify_that_below_the_Player_Name_Stats_related_to_that_Market_and_Show_Stats_is_displayed(Common):
    """
    TR_ID: C64569656
    NAME: Verify that below the Player Name Stats related to that Market and 'Show Stats' is displayed
    DESCRIPTION: Test case verifies Show Stats' is displayed for each player market
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be Configure in CMS
    PRECONDITIONS: Goals
    PRECONDITIONS: Goals inside the box
    PRECONDITIONS: Goals outside the box
    PRECONDITIONS: Offsides
    PRECONDITIONS: Passes
    PRECONDITIONS: Shots
    PRECONDITIONS: Shots on target
    PRECONDITIONS: Shots outside the box
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the Markets
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
        EXPECTED: * Stats related to the Market should be displayed for that Player
        EXPECTED: Example if its Player Total Passes Market - Passes stats for the player should be displayed
        EXPECTED: * Show Stats Link should be displayed
        """
        pass

    def test_005_validate_show_states_for_all_both_teams_team_a__team_b(self):
        """
        DESCRIPTION: Validate Show States for all Both Teams, Team A , Team B
        EXPECTED: Show stats should be displayed for all team players
        """
        pass

    def test_006_click_on_show_stats_and_come_back_from_player_states_page(self):
        """
        DESCRIPTION: Click on Show Stats and Come back from Player States page
        EXPECTED: Click on Back button in Player Stats page and come back to player bets page
        """
        pass

    def test_007_click_on_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * User should be able to click and selection should be added BYB/BB betslip
        EXPECTED: * ADDED should be displayed
        """
        pass
