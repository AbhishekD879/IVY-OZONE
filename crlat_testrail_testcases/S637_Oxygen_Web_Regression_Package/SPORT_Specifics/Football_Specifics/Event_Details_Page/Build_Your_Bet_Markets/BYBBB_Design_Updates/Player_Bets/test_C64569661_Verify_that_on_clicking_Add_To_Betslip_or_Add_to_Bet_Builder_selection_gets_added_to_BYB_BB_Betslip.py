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
class Test_C64569661_Verify_that_on_clicking_Add_To_Betslip_or_Add_to_Bet_Builder_selection_gets_added_to_BYB_BB_Betslip(Common):
    """
    TR_ID: C64569661
    NAME: Verify that on clicking  'Add To Betslip' or 'Add to Bet Builder' selection gets added to BYB/BB Betslip
    DESCRIPTION: Verify that on clicking  'Add To Betslip' or 'Add to Bet Builder' selection gets added to BYB/BB Betslip
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

    def test_004_select_any_player_name_and_add_increment_but_dont_click_on_add_to_betslip(self):
        """
        DESCRIPTION: Select any player name and add Increment but dont click on Add to Betslip
        EXPECTED: Selection should not be added to Bet Builder bet slip
        """
        pass

    def test_005_expand_any_player_market_add_selections_to_bet_builder_by_clicking_on_add_to_bet_builder_add_to_betslip_button(self):
        """
        DESCRIPTION: Expand any Player Market &&
        DESCRIPTION: ADD selections to bet builder by clicking on ADD TO BET BUILDER/ ADD TO BETSLIP button
        EXPECTED: * User should be able to click and selection should be added BYB/BB betslip
        EXPECTED: * ADDED should be displayed
        """
        pass
