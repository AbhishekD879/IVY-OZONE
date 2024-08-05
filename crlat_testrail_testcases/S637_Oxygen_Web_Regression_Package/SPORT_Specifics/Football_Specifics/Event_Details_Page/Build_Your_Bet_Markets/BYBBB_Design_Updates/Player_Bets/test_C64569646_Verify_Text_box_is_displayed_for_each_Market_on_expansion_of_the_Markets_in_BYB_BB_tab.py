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
class Test_C64569646_Verify_Text_box_is_displayed_for_each_Market_on_expansion_of_the_Markets_in_BYB_BB_tab(Common):
    """
    TR_ID: C64569646
    NAME: Verify Text box is displayed for each Market on expansion of the Markets in BYB/BB tab
    DESCRIPTION: This test case verifies text is displaying for each market on expansion of markets in BYB/BB tab
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be enabled
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the Market
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
        """
        pass

    def test_005_validate_character_limit(self):
        """
        DESCRIPTION: Validate Character Limit
        EXPECTED: &lt;&lt; Will update once character limit is set by PO&gt;&gt;
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

    def test_008_validate_when_empty_space_is_configured_in_cms_gt_byb_gt_byb_markets_gt_market_template___market_descriptionexpand_the_market(self):
        """
        DESCRIPTION: Validate when empty space is configured in CMS &gt; BYB &gt; BYB Markets &gt; Market Template - Market Description
        DESCRIPTION: Expand the Market
        EXPECTED: * Market should be Expanded
        EXPECTED: * Empty Text box should NOT be displayed
        EXPECTED: * Display should be same as for Market with no Description configured
        """
        pass
