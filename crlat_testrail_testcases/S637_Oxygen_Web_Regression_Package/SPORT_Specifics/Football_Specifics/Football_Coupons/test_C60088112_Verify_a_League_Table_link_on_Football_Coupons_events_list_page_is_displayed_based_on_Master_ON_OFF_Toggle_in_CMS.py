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
class Test_C60088112_Verify_a_League_Table_link_on_Football_Coupons_events_list_page_is_displayed_based_on_Master_ON_OFF_Toggle_in_CMS(Common):
    """
    TR_ID: C60088112
    NAME: Verify a League Table link on Football Coupons events list page is displayed based on Master ON/OFF Toggle in CMS
    DESCRIPTION: This test case verifies a League Table link on Football Coupons events list page is displayed based on ticked/unticked 'Enable' checkbox in CMS
    PRECONDITIONS: * Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: * Statistic Link is configured at least for one Coupon and one League (CMS -> Statistics Links -> League Links) (e.g. "English Premier League")
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: 1. User is on the Football Coupons tab
    """
    keep_browser_open = True

    def test_001_navigate_to_one_of_the_coupon_pages_under_todays_coupons_or_popular_coupons(self):
        """
        DESCRIPTION: Navigate to one of the Coupon pages under "Today's Coupons" or "Popular Coupons"
        EXPECTED: * Coupons page is loaded
        EXPECTED: * The list of events is displayed and grouped within Leagues accordions
        EXPECTED: * 'LEAGUES TABLE' link is displayed for configured League between <League name> and first Event Card
        """
        pass

    def test_002_navigate_to_cms___system_configuration___config___statisticslinksturn_the_master_toggle_off_for_leagues_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS -> System Configuration -> Config -> StatisticsLinks
        DESCRIPTION: Turn the master toggle OFF for leagues and save changes
        EXPECTED: Master toggle is disabled
        """
        pass

    def test_003_navigate_to_the_coupon_page_from_step_1(self):
        """
        DESCRIPTION: Navigate to the Coupon page (from Step 1)
        EXPECTED: * Coupons page is loaded
        EXPECTED: * The list of events is displayed and grouped within Leagues accordions
        EXPECTED: * 'LEAGUES TABLE' link is NOT displayed for configured League
        """
        pass

    def test_004_navigate_to_cms___system_configuration___config___statisticslinksturn_the_master_toggle_on_for_leagues_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS -> System Configuration -> Config -> StatisticsLinks
        DESCRIPTION: Turn the master toggle ON for leagues and save changes
        EXPECTED: Master toggle is enabled
        """
        pass

    def test_005_navigate_to_the_coupon_page_from_step_1(self):
        """
        DESCRIPTION: Navigate to the Coupon page (from Step 1)
        EXPECTED: * Coupons page is loaded
        EXPECTED: * The list of events is displayed and grouped within Leagues accordions
        EXPECTED: * 'LEAGUES TABLE' link IS displayed for configured League between <League name> and first Event Card
        """
        pass

    def test_006_navigate_to_cms___statistics_links___league_linksremove_configured_league_link_eg_english_premier_league(self):
        """
        DESCRIPTION: Navigate to CMS -> Statistics Links -> League Links
        DESCRIPTION: Remove configured League Link (e.g. "English Premier League")
        EXPECTED: League Link is removed from the table
        """
        pass

    def test_007_navigate_to_the_coupon_page_from_step_1(self):
        """
        DESCRIPTION: Navigate to the Coupon page (from Step 1)
        EXPECTED: * Coupons page is loaded
        EXPECTED: * The list of events is displayed and grouped within Leagues accordions
        EXPECTED: * 'LEAGUES TABLE' link is NOT displayed for configured League
        """
        pass
