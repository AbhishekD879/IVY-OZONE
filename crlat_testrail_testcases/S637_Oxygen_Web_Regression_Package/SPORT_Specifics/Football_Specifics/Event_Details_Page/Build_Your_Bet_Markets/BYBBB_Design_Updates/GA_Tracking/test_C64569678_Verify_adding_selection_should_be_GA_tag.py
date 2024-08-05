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
class Test_C64569678_Verify_adding_selection_should_be_GA_tag(Common):
    """
    TR_ID: C64569678
    NAME: Verify adding selection should be GA tag
    DESCRIPTION: This test case verifies adding of selection is Ga Tracked
    PRECONDITIONS: 1: Banach events should be available with all or ANY of the Markets
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

    def test_004_add_few_combinable_selections_to_bybbet_builder_to__dashboard_from_any_of_the_markets_accordions_and_add_them_to__betslip(self):
        """
        DESCRIPTION: Add few combinable selections to BYB/Bet Builder to  Dashboard from any of the markets accordions and add them to  betslip
        EXPECTED: * Selected selections are highlighted within accordions and added to betslip
        """
        pass

    def test_005_validate_ga_tracking_in_console_on_selecting_the_selection(self):
        """
        DESCRIPTION: Validate Ga Tracking in console on selecting the selection
        EXPECTED: * Selection should be Highlighted and Ga Tagged
        EXPECTED: ![](index.php?/attachments/get/eee14d95-6754-424b-9698-81eae90d54d1)
        """
        pass
