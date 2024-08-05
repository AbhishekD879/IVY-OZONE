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
class Test_C64569607_Verify_the_text_displayed_under_Markets_label(Common):
    """
    TR_ID: C64569607
    NAME: Verify the text displayed under 'Markets' label
    DESCRIPTION: This test case verifies the display of description under 'Markets' label
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: In CMS Market label text should be configured CMS&gt; SYSTEM CONFIGURATION
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
        EXPECTED: EDP page should be displayed with BB/BYB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: * BYB/BB tab should be displayed with all the Markets
        EXPECTED: * Build Your Bet - Combine selections to create your own unique bet! text should be displayed
        """
        pass

    def test_004_validate_the_display_of_text_under_market_label(self):
        """
        DESCRIPTION: Validate the display of text under 'Market' label
        EXPECTED: * Market Label should be displayed as per Zeplin
        EXPECTED: * Description under Market label should be displayed as configured in CMS
        EXPECTED: ![](index.php?/attachments/get/a0483b70-b5f1-4100-b55d-74d0dd8671bc) ![](index.php?/attachments/get/089b56ac-0b09-469e-bd0a-454b8fcda56e)
        """
        pass
