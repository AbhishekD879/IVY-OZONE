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
class Test_C60088573_Verify_a_link_to_Market_Statistic_on_the_EDP_is_displayed_based_on_data_available_in_scoreboard_overlay_response(Common):
    """
    TR_ID: C60088573
    NAME: Verify a link to Market Statistic on the EDP is displayed based on data available in '</scoreboard-overlay>'  response
    DESCRIPTION: This test case verifies the link to Market Statistic on the EDP is displayed based on data available in '</scoreboard-overlay>'  response
    PRECONDITIONS: - Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: - Market Link is configured at least for one Market (CMS -> Statistics Links -> Market Links)
    PRECONDITIONS: - There should not be any statistic for configured Market Link in '</scoreboard-overlay>' response (e.g. use Charles for replacing response data)
    PRECONDITIONS: Notes:
    PRECONDITIONS: (Full list of Markets Name, templateMarketName, tabKey, and overlay key are attached in the Story https://jira.egalacoral.com/browse/BMA-56388)
    PRECONDITIONS: DESIGN ASSETS: https://app.zeplin.io/project/5b850aab34c8140978c022a8/dashboard
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
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

    def test_002_click_the_view_statistics_linknotethere_should_not_be_any_statistics_for_this_market(self):
        """
        DESCRIPTION: Click the 'View Statistics' link
        DESCRIPTION: **Note:**
        DESCRIPTION: there should not be any statistics for this market
        EXPECTED: * Statistics data is not displayed
        EXPECTED: * 'No data available for this competition' text is displayed
        """
        pass
