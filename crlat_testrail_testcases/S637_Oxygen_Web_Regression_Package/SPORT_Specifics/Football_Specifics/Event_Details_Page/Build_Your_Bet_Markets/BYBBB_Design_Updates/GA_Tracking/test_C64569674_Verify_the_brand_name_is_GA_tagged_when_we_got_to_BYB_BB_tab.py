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
class Test_C64569674_Verify_the_brand_name_is_GA_tagged_when_we_got_to_BYB_BB_tab(Common):
    """
    TR_ID: C64569674
    NAME: Verify the brand name is GA tagged when we got to BYB/BB tab
    DESCRIPTION: This test case Verifies the Brand name is Ga Tagged when we click on BYB/BB tab
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

    def test_004_validate_ga_tracking_in_console_for_the_brand_name_in_bybbb_tab(self):
        """
        DESCRIPTION: Validate GA tracking in Console for the brand name in BYB/BB tab
        EXPECTED: * Brand should be Ga Tagged when we click on BYB/BB tab
        EXPECTED: ![](index.php?/attachments/get/5f2da190-e1bd-4446-8dc1-ea283a025270)
        """
        pass
