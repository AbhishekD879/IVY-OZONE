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
class Test_C64569620_Verify_that_under_Popular_Markets_filter_the_markets_configured_in_CMS_with_Popular_Markets_are_ONLY_displayed(Common):
    """
    TR_ID: C64569620
    NAME: Verify that under 'Popular Markets' filter the markets configured in CMS with Popular Markets are ONLY displayed
    DESCRIPTION: This test case verifies the display of Popular Markets filter
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: In CMS one or more Markets should be configured with Popular Markets
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
        EXPECTED: BYB/BB tab should be displayed with all the Markets
        """
        pass

    def test_004_click_on_popular_markets(self):
        """
        DESCRIPTION: Click on Popular Markets
        EXPECTED: * Popular Markets should be displayed and highlighted
        EXPECTED: * Markets which are configured in CMS ONLY should be displayed
        """
        pass

    def test_005_in_cms_disable_popular_markets_for_any_one_of_the_market_and_validate_the_display_of_that_market_in_popular_markets_filter(self):
        """
        DESCRIPTION: In CMS disable Popular Markets for any one of the Market and Validate the display of that market in Popular Markets filter
        EXPECTED: * User should be able to make the changes in CMS successfully
        EXPECTED: * Market should no longer be displayed in Popular Markets tab
        EXPECTED: * Market should be still displayed in All Markets tab
        """
        pass
