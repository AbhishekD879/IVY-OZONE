import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60088114_Verify_a_link_to_Market_Statistic_on_the_EDP(Common):
    """
    TR_ID: C60088114
    NAME: Verify a link to Market Statistic on the EDP
    DESCRIPTION: This test case verifies the link to Market Statistic on the EDP
    PRECONDITIONS: - Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: - Market Link is configured at least for one Market (CMS -> Statistics Links -> Market Links)
    PRECONDITIONS: (Full list of Markets Name, templateMarketName, tabKey, and overlay key are attached in the Story https://jira.egalacoral.com/browse/BMA-56388)
    PRECONDITIONS: DESIGN ASSETS: https://app.zeplin.io/project/5b850aab34c8140978c022a8/dashboard
    PRECONDITIONS: Notes:
    PRECONDITIONS: * Example of 'market-links' response:
    PRECONDITIONS: https://cms-dev1.coral.co.uk/cms/api/bma/market-links
    PRECONDITIONS: - Opta Event is subscribed
    PRECONDITIONS: 1. The user is on the Football EDP
    """
    keep_browser_open = True

    def test_001_verify_that_the_view_statistics_is_displayed_for_the_market_with_configured_market_link_from_precondition(self):
        """
        DESCRIPTION: Verify that the 'View Statistics' is displayed for the Market with configured Market link (from precondition)
        EXPECTED: The 'View Statistics' link is displayed according to the design:
        EXPECTED: Ladbrokes Desktop/Mobile:
        EXPECTED: ![](index.php?/attachments/get/122180525)
        EXPECTED: ![](index.php?/attachments/get/122180524)
        EXPECTED: Coral Desktop:
        EXPECTED: ![](index.php?/attachments/get/122180526)
        """
        pass

    def test_002_click_on_the_view_statisticslink_name_configured_in_cms_on_the_market_from_precondition(self):
        """
        DESCRIPTION: Click on the 'View Statistics'(Link Name configured in CMS) on the Market (from precondition)
        EXPECTED: Statistic data is displayed (if available)
        """
        pass

    def test_003_navigate_to_console_and_observe_the_market_links_response(self):
        """
        DESCRIPTION: Navigate to console and observe the 'market-links' response:
        EXPECTED: e.g.
        EXPECTED: {marketName: "Match Result", linkName: "show statistics1", tabKey: "latest-forms",…}
        EXPECTED: linkName: "show statistics1"
        EXPECTED: marketName: "Match Result"
        EXPECTED: overlayKey: "latestForm"
        EXPECTED: tabKey: "latest-forms"
        """
        pass

    def test_004_click_the_x_close_button(self):
        """
        DESCRIPTION: Click the 'x' close button
        EXPECTED: Market Statistic Link Popup is closed
        """
        pass
