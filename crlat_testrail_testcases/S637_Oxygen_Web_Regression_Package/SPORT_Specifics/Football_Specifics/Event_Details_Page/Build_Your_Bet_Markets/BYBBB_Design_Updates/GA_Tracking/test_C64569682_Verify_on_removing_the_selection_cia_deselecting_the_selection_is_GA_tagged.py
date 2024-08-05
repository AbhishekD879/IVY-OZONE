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
class Test_C64569682_Verify_on_removing_the_selection_cia_deselecting_the_selection_is_GA_tagged(Common):
    """
    TR_ID: C64569682
    NAME: Verify on removing the selection  cia deselecting the selection is GA tagged
    DESCRIPTION: This test case verifies deselecting of the selection should be Ga Tracked
    PRECONDITIONS: 1:Banach events should be available with all or ANY of the above Markets
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

    def test_004_click_on_any_of_the_player_market_either_from_all_markets_filter_or_player_bets_filter(self):
        """
        DESCRIPTION: Click on ANY of the Player Market either from All Markets filter or Player Bets filter
        EXPECTED: * Market should be expanded
        """
        pass

    def test_005_add_few_combinable_selections_to_bybbet_builder_to__dashboard_from_different_markets_accordions_and_add_them_to__betslip(self):
        """
        DESCRIPTION: Add few combinable selections to BYB/Bet Builder to  Dashboard from different markets accordions and add them to  betslip
        EXPECTED: * Selected selections are highlighted within accordions and added to betslip
        """
        pass

    def test_006_verify_the_build_your_bet_for_coral_bet_builderfor_lads_click_on_dashboard_content_area_to_expand_the_betslip(self):
        """
        DESCRIPTION: Verify the Build Your Bet (for Coral)/ Bet Builder(for lads) click on Dashboard content area to expand the betslip
        EXPECTED: * Dashboard  content area should be expanded where the selections are added
        """
        pass

    def test_007_validate_on_selecting_the_selection_should_highlighted(self):
        """
        DESCRIPTION: Validate on selecting the selection should Highlighted
        EXPECTED: * Selection should be Highlighted and Ga Tagged
        """
        pass

    def test_008_validate_ga_tracking_in_console_for_deselecting_the_selection(self):
        """
        DESCRIPTION: Validate Ga Tracking in console for deselecting the selection
        EXPECTED: * On removing the selection via deselecting its should be Ga tagged
        EXPECTED: ![](index.php?/attachments/get/ebb243b3-c29c-4773-9523-5afc5425ff99)
        """
        pass
