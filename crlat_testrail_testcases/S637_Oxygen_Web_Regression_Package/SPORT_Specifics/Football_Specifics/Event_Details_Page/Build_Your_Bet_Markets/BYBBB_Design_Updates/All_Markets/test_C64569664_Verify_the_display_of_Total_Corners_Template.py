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
class Test_C64569664_Verify_the_display_of_Total_Corners_Template(Common):
    """
    TR_ID: C64569664
    NAME: Verify the display of Total Corners Template
    DESCRIPTION: This test case verifies the display of Total Corners Template
    PRECONDITIONS: 1: BYB/BB Markets should be available for any event
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
        EXPECTED: EDP page should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB Markets should be displayed
        """
        pass

    def test_004_validate_the_new_template_for_total_corners_market_as_per_zeplin(self):
        """
        DESCRIPTION: Validate the new template for Total Corners Market as per zeplin
        EXPECTED: * Select Team Text should be displayed and selections should be displayed below
        EXPECTED: * Time Period Text should be displayed and Selections should be displayed below
        """
        pass

    def test_005_validate_the_display_of_corners(self):
        """
        DESCRIPTION: Validate the display of Corners
        EXPECTED: * Corners should be displayed with Over , Exactly & Under selections when the User selects Time period
        """
        pass

    def test_006_validate_the_increment_based_on_over_exactly_and_under_selections(self):
        """
        DESCRIPTION: Validate the increment based on Over, Exactly and Under Selections
        EXPECTED: **Exactly**
        EXPECTED: * When Exactly is selected Increments text should be displayed in whole number 1,2,3...
        EXPECTED: * Increments of 1 should be displayed
        EXPECTED: **Over and Under**
        EXPECTED: * When Over/Under selection is selected Increments should be displayed in Decimals 0.5,1,1.5
        EXPECTED: * Increments of 0.5 should be displayed
        """
        pass

    def test_007_validate_add_to_bet_builder_add_to_betslip_cta_button(self):
        """
        DESCRIPTION: Validate ADD TO BET BUILDER/ ADD TO BETSLIP CTA button
        EXPECTED: * ADD TO BET BUILDER/ ADD TO BETSLIP should be displayed
        EXPECTED: * On clicking ADD TO BET BUILDER/ ADD TO BETSLIP it should be added to Betslip
        """
        pass
