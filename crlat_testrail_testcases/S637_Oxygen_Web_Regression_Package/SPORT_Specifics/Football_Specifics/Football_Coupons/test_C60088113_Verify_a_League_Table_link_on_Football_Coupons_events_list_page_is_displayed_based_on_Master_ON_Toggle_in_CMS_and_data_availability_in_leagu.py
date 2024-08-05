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
class Test_C60088113_Verify_a_League_Table_link_on_Football_Coupons_events_list_page_is_displayed_based_on_Master_ON_Toggle_in_CMS_and_data_availability_in_leaguetable_response(Common):
    """
    TR_ID: C60088113
    NAME: Verify a League Table link on Football Coupons events list page is displayed based on Master ON Toggle in CMS and data availability in 'leaguetable'  response
    DESCRIPTION: This test case verifies a League Table link on Football Coupons events list page is displayed based on ticked/unticked 'Enable' checkbox in CMS and data availability in 'leaguetable' response
    PRECONDITIONS: * Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: * Statistic Link is configured at least for one Coupon and one League (CMS -> Statistics Links -> League Links) (e.g. "English Premier League")
    PRECONDITIONS: * There should not be any statistic for configured League Link in 'leaguetable' response (e.g. use Charles for replacing response data)
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

    def test_002_click_the_leagues_table_link_eg_english_premier_leaguenotethere_should_not_be_any_statistics_for_this_league(self):
        """
        DESCRIPTION: Click the 'LEAGUES TABLE' link (e.g. "English Premier League")
        DESCRIPTION: **Note:**
        DESCRIPTION: there should not be any statistics for this league
        EXPECTED: * League Table popup with the League Table relevant to the competition for which the button was pressed, for example, "English Premier League" is displayed
        EXPECTED: * Statistics data is not displayed
        EXPECTED: * 'No data available for this competition' text is displayed
        """
        pass
