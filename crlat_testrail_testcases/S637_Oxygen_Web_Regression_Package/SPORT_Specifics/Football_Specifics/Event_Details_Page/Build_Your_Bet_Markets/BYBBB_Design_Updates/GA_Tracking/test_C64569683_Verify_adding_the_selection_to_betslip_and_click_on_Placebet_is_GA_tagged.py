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
class Test_C64569683_Verify_adding_the_selection_to_betslip_and_click_on_Placebet_is_GA_tagged(Common):
    """
    TR_ID: C64569683
    NAME: Verify adding the selection to betslip and click on Placebet is GA tagged
    DESCRIPTION: This test case verifies adding the selection to betslip should be Ga tracked
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

    def test_006_validate_on_adding_the_selection_to_betslip_and_clicking_on_placebet_should_be_tagged(self):
        """
        DESCRIPTION: Validate on adding the selection to betslip and clicking on placebet should be Tagged
        EXPECTED: * Selection Added to betslip and click on placebet should be Ga Tagged
        EXPECTED: ![](index.php?/attachments/get/7064b785-f6f2-4d0e-af24-63d1139acc1c)
        """
        pass
