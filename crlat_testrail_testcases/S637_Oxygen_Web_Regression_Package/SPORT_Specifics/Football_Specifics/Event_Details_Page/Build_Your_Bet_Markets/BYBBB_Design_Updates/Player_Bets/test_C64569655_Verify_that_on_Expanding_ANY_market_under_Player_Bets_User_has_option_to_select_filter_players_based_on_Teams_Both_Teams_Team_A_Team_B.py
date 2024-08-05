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
class Test_C64569655_Verify_that_on_Expanding_ANY_market_under_Player_Bets_User_has_option_to_select_filter_players_based_on_Teams_Both_Teams_Team_A_Team_B(Common):
    """
    TR_ID: C64569655
    NAME: Verify that on Expanding ANY market under Player Bets, User has option to select/filter players based on Teams (Both Teams, Team A , Team B)
    DESCRIPTION: Test case verifies User has option to select/filter players based on Teams (Both Teams, Team A , Team B)
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

    def test_004_validate_the_filters_both_teams_team_a__team_b(self):
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

    def test_005_expand_the_player_name_by_clicking_on_the_chevron_from_each_filter(self):
        """
        DESCRIPTION: Expand the Player name by clicking on the chevron from each filter
        EXPECTED: * Player Name should be Expanded
        EXPECTED: * Stats Increment should be displayed
        EXPECTED: * Increments of 1 should be displayed
        EXPECTED: * ADD TO BET BUILDER/ ADD TO BETSLIP CTA should be displayed
        """
        pass

    def test_006_select_stats___increase__decrease__click_on_plus___(self):
        """
        DESCRIPTION: Select Stats - Increase / Decrease -Click on (+) / (-)
        EXPECTED: * User should be able to click on (+) / (-)
        EXPECTED: * Depending on the Min /Max Stats (+) / (-) should be disabled after crossing the increments
        """
        pass

    def test_007_click_on_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * User should be able to click and selection should be added BYB/BB betslip
        EXPECTED: * ADDED should be displayed
        """
        pass

    def test_008_click_on_show_more(self):
        """
        DESCRIPTION: Click on Show More
        EXPECTED: * By default &lt;TBD&gt; players should be displayed
        EXPECTED: * More Players should be loaded on clicking Show More
        EXPECTED: * Show Less should be displayed
        """
        pass
