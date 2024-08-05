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
class Test_C64569650_Verify_that_Player_names_are_displayed_as_per_5_A_side_logic(Common):
    """
    TR_ID: C64569650
    NAME: Verify that Player names are displayed as per 5-A side logic
    DESCRIPTION: Verify that Player names are displayed as per 5-A side logic
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

    def test_005_expand_the_player_name_by_clicking_on_the_chevron(self):
        """
        DESCRIPTION: Expand the Player name by clicking on the chevron
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

    def test_008_validate_the_display_order_of_players(self):
        """
        DESCRIPTION: Validate the display order of Players
        EXPECTED: * Players should be displayed as per 5-A side Order
        EXPECTED: * Player with highest stats should be displayed first
        EXPECTED: Logic for player name display - This should be in price order (shortest price at the top of the list) and if there are two or more players with the same price we sort by name (Alphabetical order)
        """
        pass
