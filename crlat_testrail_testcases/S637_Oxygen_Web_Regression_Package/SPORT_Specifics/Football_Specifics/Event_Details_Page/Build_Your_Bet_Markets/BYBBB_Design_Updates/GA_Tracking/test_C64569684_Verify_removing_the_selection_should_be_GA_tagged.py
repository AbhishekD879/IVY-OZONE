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
class Test_C64569684_Verify_removing_the_selection_should_be_GA_tagged(Common):
    """
    TR_ID: C64569684
    NAME: Verify removing the selection should be GA tagged
    DESCRIPTION: 
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
        EXPECTED: * User should be navigated to EDP
        EXPECTED: * Build Your Bet /Bet Builder tab should be displayed
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: * BYB/BB tab should be displayed
        EXPECTED: * Filters should be displayed
        EXPECTED: * All Markets tab should be displayed by default
        """
        pass

    def test_004_validate_the_brand_is_ga_tagged_for_bybbb(self):
        """
        DESCRIPTION: Validate the brand is Ga tagged for BYB/BB
        EXPECTED: * Brand should be Ga Tagged when we click on BYB/BB tab
        """
        pass

    def test_005_validate_toggle_between_the_filters_all_marketspopular_marketsplayer_betsteam_bets_is_ga_tagged(self):
        """
        DESCRIPTION: Validate toggle between the filters (All Markets,Popular markets,Player bets,team bets) is Ga Tagged
        EXPECTED: Toggle between the filters should be Ga tagged
        """
        pass

    def test_006_validate_expansioncollapse_with_the_market_accordions_is_ga_tagged_in_bybbb(self):
        """
        DESCRIPTION: Validate Expansion/Collapse with the market accordions is Ga Tagged in BYB/BB
        EXPECTED: * When expansion/Collapse of the market should Ga Tagged
        """
        pass

    def test_007_validate_on_interaction_with_show_stats_for_the_player_is_ga_tagged(self):
        """
        DESCRIPTION: Validate on interaction with 'Show Stats' for the player is Ga Tagged
        EXPECTED: * Show Stats for the player is Ga tagged
        """
        pass

    def test_008_validate_on_selecting_the_selection_should_be__ga_tagged(self):
        """
        DESCRIPTION: Validate on selecting the selection should be  Ga Tagged
        EXPECTED: * Selection should be Highlighted and Ga Tagged
        """
        pass

    def test_009_validate_openingclosing_of_the_quick_bet_after_adding_the_selections_should_be_ga_tagged(self):
        """
        DESCRIPTION: Validate Opening/Closing of the Quick bet after adding the selections should be Ga tagged
        EXPECTED: * Opening/Closing of the Dashboard for quick bet should be GA Tagged
        """
        pass

    def test_010_validate_editing_the_selection_from_bybbb_quick_bet(self):
        """
        DESCRIPTION: validate Editing the selection from BYB/BB quick bet
        EXPECTED: * Editing the selection should be Ga Tagged
        """
        pass

    def test_011_validate_when_customer_click_on_done_after_editing_the_selection_in_bybbb_quick_bet_is_ga_tagged(self):
        """
        DESCRIPTION: Validate when customer click on Done after editing the selection in BYB/BB quick bet is GA tagged
        EXPECTED: * Click on Done after editing the selection should be GA tagged in Quick bet BYB/BB
        """
        pass

    def test_012_validate__remove_button_is_clicked_for_the_selection_inside_dashboard(self):
        """
        DESCRIPTION: Validate  "Remove" button is clicked for the selection inside dashboard
        EXPECTED: * Click on "Remove" button for the selection inside dashboard ,On removing selecton  it should be Ga tagged
        """
        pass

    def test_013_validate_deselecting_the_selection_is_ga_tagged(self):
        """
        DESCRIPTION: Validate deselecting the selection is Ga Tagged
        EXPECTED: * On removing the selection via deselecting its should be Ga tagged
        """
        pass

    def test_014_validate_on_adding_the_selection_to_betslip_should_be_tagged(self):
        """
        DESCRIPTION: Validate on adding the selection to betslip should be Tagged
        EXPECTED: * Selection Added to betslip should be Ga Tagged
        """
        pass

    def test_015_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
