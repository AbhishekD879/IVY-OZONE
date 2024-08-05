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
class Test_C64569665_Verify_the_display_of_Correct_Score_Template(Common):
    """
    TR_ID: C64569665
    NAME: Verify the display of Correct Score Template
    DESCRIPTION: This test case verifies the display of Correct Score template
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

    def test_004_validate_the_new_template_for_correct_score_market_as_per_zeplin(self):
        """
        DESCRIPTION: Validate the new template for Correct Score Market as per zeplin
        EXPECTED: * Time Period Text should be displayed with selections displayed below
        EXPECTED: * Score should be displayed and Increments for both Teams
        EXPECTED: * ADD TO BET BUILDER / ADD TO BETSLIP CTA should be displayed
        EXPECTED: ![](index.php?/attachments/get/eb655255-4a65-4490-92cb-a63b98bc2a55) ![](index.php?/attachments/get/87d1a94c-cad9-4365-8919-c1a2b79f9405)
        """
        pass
