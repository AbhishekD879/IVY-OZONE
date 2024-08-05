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
class Test_C64569660_Verify_that_Add_To_Betslip_or_Add_to_Bet_Builder_CTA_is_displayed(Common):
    """
    TR_ID: C64569660
    NAME: Verify that 'Add To Betslip' or 'Add to Bet Builder' CTA is displayed
    DESCRIPTION: Verify that 'Add To Betslip' or 'Add to Bet Builder' CTA is displayed
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

    def test_004_verify_if_there_are_two_or_more_players_with_the_same_price_we_sort_by_name_alphabetical_order(self):
        """
        DESCRIPTION: Verify if there are two or more players with the same price we sort by name (Alphabetical order)
        EXPECTED: Player name should be Sorted by Alphabetical Order
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

    def test_006_verify_team_jersey_and_player_positions(self):
        """
        DESCRIPTION: Verify team jersey and Player positions
        EXPECTED: Team jersey image should be displayed before Players name followed by player position.
        """
        pass

    def test_007_verify_bet_is_added_to_bet_slip_after_user_selected_player_name_and_added_increment(self):
        """
        DESCRIPTION: Verify bet is added to bet slip after User selected player name and added increment
        EXPECTED: Bet should not be added to BYB bet slip until click on Add to Bet slip /Add to Bet Builder Button
        """
        pass
