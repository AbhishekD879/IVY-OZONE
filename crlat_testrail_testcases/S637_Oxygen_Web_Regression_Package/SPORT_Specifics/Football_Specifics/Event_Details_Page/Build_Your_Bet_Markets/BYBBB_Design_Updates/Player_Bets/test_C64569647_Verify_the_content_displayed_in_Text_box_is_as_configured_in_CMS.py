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
class Test_C64569647_Verify_the_content_displayed_in_Text_box_is_as_configured_in_CMS(Common):
    """
    TR_ID: C64569647
    NAME: Verify the content displayed in Text box is as configured in CMS
    DESCRIPTION: This test case verifies the market content text is displayed as per CMS configuration
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be enabled
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the Markets
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
        EXPECTED: * Market label should be displayed with description below it
        EXPECTED: * All Markets Filter should be displayed and highlighted by default
        EXPECTED: * Player Bets, Popular Markets , Team Bets filter should be displayed based on the CMS configurations
        """
        pass

    def test_004_expand_any_market_which_has_market_description_configured_in_cms(self):
        """
        DESCRIPTION: Expand any Market which has Market Description configured in CMS
        EXPECTED: * Market should be Expanded
        EXPECTED: * Description should be displayed as configured in CMS
        EXPECTED: * CSS should be as per Zeplin
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/b70ddb17-1ec8-4824-adc8-81ef4f64f1b1)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/cabd9904-0281-4919-8d2f-d7dc34b58087)
        """
        pass
