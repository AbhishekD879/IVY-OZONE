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
class Test_C64569668_Verify_the_display_of_Total_Goals_Template(Common):
    """
    TR_ID: C64569668
    NAME: Verify the display of Total Goals Template
    DESCRIPTION: This test case verifies the display of Total Goals Template
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: EDP page should be displayed with BYB/BB tab
        """
        pass

    def test_003_validate_the_display_of_total_goals_template_in_bybbb_markets(self):
        """
        DESCRIPTION: Validate the display of Total Goals template in BYB/BB Markets
        EXPECTED: * Select Team should be displayed with selections below
        EXPECTED: * Time Period should be displayed with selections below
        EXPECTED: ![](index.php?/attachments/get/dea7de6e-3c60-4b0e-9aa0-877c6f8dd3d8)
        """
        pass

    def test_004_validate_the_display_of_goals(self):
        """
        DESCRIPTION: Validate the display of Goals
        EXPECTED: * Goals should be displayed with Over , Exactly & Under selections when the User selects Time period
        """
        pass

    def test_005_validate_the_increment_based_on_over_exactly_and_under_selections(self):
        """
        DESCRIPTION: Validate the increment based on Over, Exactly and Under Selections
        EXPECTED: **Exactly**
        EXPECTED: * When Exactly is selected Increments text should be displayed in whole number 1,2,3...
        EXPECTED: * Increments of 1 should be displayed
        EXPECTED: **Over and Under**
        EXPECTED: * When Over/Under selection is selected Increments should be displayed in Decimals 0.5,1,1.5
        EXPECTED: * Increments of 0.5 should be displayed
        EXPECTED: ![](index.php?/attachments/get/8f6ad8b0-3816-47ae-9a6e-2e6385d6c3c8)
        """
        pass

    def test_006_validate_the_display_of_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Validate the display of ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * ADD TO BET BUILDER/ADD TO Betslip should be enabled after selecting the selections from Select Team, Time Period & Goals
        EXPECTED: ![](index.php?/attachments/get/3f41b3f9-ec77-4412-8818-18d4d9d97271)
        """
        pass
