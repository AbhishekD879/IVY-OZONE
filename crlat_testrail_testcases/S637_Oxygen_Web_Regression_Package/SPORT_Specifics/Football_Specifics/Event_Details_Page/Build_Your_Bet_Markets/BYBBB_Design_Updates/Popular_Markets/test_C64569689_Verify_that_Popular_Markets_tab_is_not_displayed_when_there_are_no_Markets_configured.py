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
class Test_C64569689_Verify_that_Popular_Markets_tab_is_not_displayed_when_there_are_no_Markets_configured(Common):
    """
    TR_ID: C64569689
    NAME: Verify that Popular Markets tab is not displayed when there are no Markets configured
    DESCRIPTION: 
    PRECONDITIONS: 1: Popular Markets should be disabled for all markets in CMS &gt; BYB &gt; BYB Markets
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_gt_byb_gt_byb_markets__popular_market_flag_disable_for_all_the_markets(self):
        """
        DESCRIPTION: Navigate to CMS &gt; BYB &gt; BYB Markets  Popular market flag Disable for all the markets
        EXPECTED: Popular market flag should be disable for all the markets
        """
        pass

    def test_002_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral Application
        EXPECTED: User should be able to Launch the Ladbrokes/Coral successfully
        """
        pass

    def test_003_navigate_to_any_event_which_has_byb_markets_gt_edp(self):
        """
        DESCRIPTION: Navigate to ANY event which has BYB markets &gt; EDP
        EXPECTED: User should be able to navigate to Football Event Details page
        """
        pass

    def test_004_click_on_build_your_bet_or_bet_builder(self):
        """
        DESCRIPTION: Click on Build Your Bet or Bet Builder
        EXPECTED: * Bet Builder/Build Your Bet tab should be opened
        """
        pass

    def test_005_validate_the_display_of_bybbb_tab(self):
        """
        DESCRIPTION: Validate the display of BYB/BB tab
        EXPECTED: * Filters should be displayed based on the CMS configuration
        EXPECTED: * All Markets should be selected by default
        """
        pass

    def test_006_check_the_popular_markets_tab(self):
        """
        DESCRIPTION: Check the Popular Markets tab
        EXPECTED: * Popular Markets should not be displayed
        EXPECTED: * Remaining Filters should be displayed
        """
        pass
