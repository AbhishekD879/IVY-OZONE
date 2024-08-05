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
class Test_C64569606_Verify_that_Markets_label_is_displayed_under_BYB_BB_tab_as_per_the_Zeplin_design(Common):
    """
    TR_ID: C64569606
    NAME: Verify that 'Markets' label is displayed under BYB/BB tab as per the Zeplin design
    DESCRIPTION: This test case verifies the display of Market Label in BYB/BB tab
    PRECONDITIONS: 1: BYB/BB Market should be available for the event
    PRECONDITIONS: 2: Market Description should be configured in CMS &gt; System Configuration (Market Label)
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
        EXPECTED: * BYB/BB Markets page should be displayed
        EXPECTED: * Build Your Bet - Combine selections to create your own unique bet! text should be displayed
        """
        pass

    def test_004_validate_the_display_of_market_label(self):
        """
        DESCRIPTION: Validate the display of Market label
        EXPECTED: * Market Label should be displayed as per Zeplin
        EXPECTED: * Description under Market label should be displayed as configured in CMS
        EXPECTED: ![](index.php?/attachments/get/0946b0f1-f142-4272-8da5-84dc8936ebab) ![](index.php?/attachments/get/b8de9942-b666-4d23-bb64-f4d48b9dfcc1)
        """
        pass
