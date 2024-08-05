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
class Test_C60088572_Verify_a_link_to_Market_Statistic_on_the_EDP_is_displayed_based_on_Master_ON_OFF_Toggle_in_CMS(Common):
    """
    TR_ID: C60088572
    NAME: Verify a link to Market Statistic on the EDP is displayed based on Master ON/OFF Toggle in CMS
    DESCRIPTION: This test case verifies the link to Market Statistic on the EDP is displayed based on Master ON/OFF Toggle in CMS
    PRECONDITIONS: - Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: - Market Link is configured at least for one Market (CMS -> Statistics Links -> Market Links)
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

    def test_002_navigate_to_cms___system_configuration___config___statisticslinksturn_the_master_toggle_off_for_markets_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS -> System Configuration -> Config -> StatisticsLinks
        DESCRIPTION: Turn the master toggle OFF for markets and save changes
        EXPECTED: Master toggle is disabled
        """
        pass

    def test_003_return_to_edp_from_step_1(self):
        """
        DESCRIPTION: Return to EDP from step 1
        EXPECTED: The 'View Statistics' link is NOT displayed for configured market
        """
        pass

    def test_004_navigate_to_cms___system_configuration___config___statisticslinksturn_the_master_toggle_on_for_markets_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS -> System Configuration -> Config -> StatisticsLinks
        DESCRIPTION: Turn the master toggle ON for markets and save changes
        EXPECTED: Master toggle is enabled
        """
        pass

    def test_005_return_to_edp_from_step_1(self):
        """
        DESCRIPTION: Return to EDP from step 1
        EXPECTED: The 'View Statistics' link IS displayed for configured market
        """
        pass

    def test_006_navigate_to_cms___statistics_links___league_linksremove_configured_market_link(self):
        """
        DESCRIPTION: Navigate to CMS -> Statistics Links -> League Links
        DESCRIPTION: Remove configured Market Link
        EXPECTED: Market Link is removed from the table
        """
        pass

    def test_007_return_to_edp_from_step_1(self):
        """
        DESCRIPTION: Return to EDP from step 1
        EXPECTED: The 'View Statistics' link is NOT displayed for configured market
        """
        pass
