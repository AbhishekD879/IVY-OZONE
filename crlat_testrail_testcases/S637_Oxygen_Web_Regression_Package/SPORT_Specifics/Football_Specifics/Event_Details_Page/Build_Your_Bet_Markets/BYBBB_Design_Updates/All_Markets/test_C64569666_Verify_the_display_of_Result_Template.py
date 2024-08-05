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
class Test_C64569666_Verify_the_display_of_Result_Template(Common):
    """
    TR_ID: C64569666
    NAME: Verify the display of Result Template
    DESCRIPTION: This test case verifies the display of Results Template
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
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

    def test_004_validate_the_display_of_results_template_as_per_zeplin(self):
        """
        DESCRIPTION: Validate the display of Results Template as per Zeplin
        EXPECTED: * Select Team text should be displayed and selections should be displayed below
        EXPECTED: * Time Period text should be displayed and selections should be displayed below
        """
        pass

    def test_005_validate_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Validate ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * ADD TO BET BUILDER/ ADD TO BETSLIP should be disabled when only one or no selections are selected from Select Team & Time Period
        EXPECTED: ![](index.php?/attachments/get/2f01fb8f-46ff-4347-b71c-7b418a0ef3c5)
        EXPECTED: * ADD TO BET BUILDER/ ADD TO BETSLIP should be enabled when selection from Select Team & Time Period are selected
        EXPECTED: ![](index.php?/attachments/get/af4d0e18-1302-4b5f-b169-86058b98b38a)
        """
        pass

    def test_006_click_on_add_to_bet_builder_add_to_betslip_when_enabled(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP (When enabled)
        EXPECTED: * User should be be able to add the bet
        EXPECTED: * ADDED should be displayed
        EXPECTED: ![](index.php?/attachments/get/640cf66e-06f2-4e61-8df7-1188186d40ee)
        """
        pass
