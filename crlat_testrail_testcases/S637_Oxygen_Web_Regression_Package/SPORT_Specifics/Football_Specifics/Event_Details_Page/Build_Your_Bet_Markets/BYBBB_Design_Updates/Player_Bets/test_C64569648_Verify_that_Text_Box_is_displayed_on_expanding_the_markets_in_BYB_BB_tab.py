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
class Test_C64569648_Verify_that_Text_Box_is_displayed_on_expanding_the_markets_in_BYB_BB_tab(Common):
    """
    TR_ID: C64569648
    NAME: Verify that Text Box is displayed on expanding the markets in BYB/BB tab
    DESCRIPTION: This test case verifies the text box display on expansion of the market for BYB/BB tab
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be enabled and configure with market description in market templet
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
        EXPECTED: ![](index.php?/attachments/get/f51d9b99-4283-403f-95ce-e4565cf1acb0)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/3b45b492-a6ce-4cd4-9087-1985bfe31aab)
        """
        pass

    def test_005_validate_market_content_text_box_is_displaying_when_market_is_expanded(self):
        """
        DESCRIPTION: Validate Market content text box is displaying when market is expanded
        EXPECTED: * Content text should be displayed when the market is expanded
        """
        pass

    def test_006_collapse_the_market(self):
        """
        DESCRIPTION: Collapse the Market
        EXPECTED: * Market should be Collapsed
        EXPECTED: * Description should not be displayed
        """
        pass

    def test_007_if_this_market_is_available_in_any_other_filter_and_expand_there_and_validate(self):
        """
        DESCRIPTION: If this Market is available in any other filter and Expand there and Validate
        EXPECTED: * Market should be Expanded
        EXPECTED: * Description should be displayed as configured in CMS
        EXPECTED: * CSS should be as per Zeplin
        """
        pass
