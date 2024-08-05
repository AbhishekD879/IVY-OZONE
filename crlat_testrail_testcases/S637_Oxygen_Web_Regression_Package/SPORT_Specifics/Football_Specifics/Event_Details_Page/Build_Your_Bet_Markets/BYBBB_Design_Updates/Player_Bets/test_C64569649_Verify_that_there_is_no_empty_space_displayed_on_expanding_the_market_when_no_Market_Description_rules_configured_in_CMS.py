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
class Test_C64569649_Verify_that_there_is_no_empty_space_displayed_on_expanding_the_market_when_no_Market_Description_rules_configured_in_CMS(Common):
    """
    TR_ID: C64569649
    NAME: Verify that there is no empty space displayed on expanding the market when no Market Description/rules configured in CMS
    DESCRIPTION: This test case verifies no space should be displayed for markets in BYB/BB tab if there is no configuration for Market description in market templet
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
        EXPECTED: * Market label should be displayed with no description below it
        EXPECTED: * All Markets Filter should be displayed and highlighted by default
        EXPECTED: * Player Bets, Popular Markets , Team Bets filter should be displayed based on the CMS configurations
        """
        pass

    def test_004_validate_when_empty_space_is_configured_in_cms_gt_byb_gt_byb_markets_gt_market_template___market_descriptionexpand_the_market(self):
        """
        DESCRIPTION: Validate when empty space is configured in CMS &gt; BYB &gt; BYB Markets &gt; Market Template - Market Description
        DESCRIPTION: Expand the Market
        EXPECTED: * Market should be Expanded
        EXPECTED: * Empty Text box should NOT be displayed
        EXPECTED: * Display should be same as for Market with no Description configured
        """
        pass
