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
class Test_C60088039_Verify_a_link_to_a_League_Table_window_in_Football_Coupon_event_list_pages(Common):
    """
    TR_ID: C60088039
    NAME: Verify a link to a League Table window in Football Coupon event list pages
    DESCRIPTION: This test case verifies a link to a League Table window in Football Coupon event list pages
    PRECONDITIONS: * Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: * Statistic Link is configured at least for one Coupon and one League (CMS -> Statistics Links -> League Links)
    PRECONDITIONS: Notes:
    PRECONDITIONS: * Example of 'league-links' response:
    PRECONDITIONS: https://<cms_domain>/cms/api/bma/league-links/<couponID>
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

    def test_002_navigate_to_console_and_observe_the_league_links_response_eg_httpscms_dev1coralcoukcmsapibmaleague_links559(self):
        """
        DESCRIPTION: Navigate to console and observe the 'league-links' response (e.g. https://cms-dev1.coral.co.uk/cms/api/bma/league-links/559)
        EXPECTED: * 'league-links' response is received
        EXPECTED: Example:
        EXPECTED: dhLeagueId: "3082"
        EXPECTED: linkName: "Championship"
        EXPECTED: obLeagueId: "435"
        EXPECTED: ![](index.php?/attachments/get/122180479)
        """
        pass

    def test_003_click_the_leagues_table_link_for_some_league_eg_english_premier_league(self):
        """
        DESCRIPTION: Click the 'LEAGUES TABLE' link for some League (e.g. "English Premier League")
        EXPECTED: * League Table popup with the League Table relevant to the competition for which the button was pressed, for example, "English Premier League" is displayed
        EXPECTED: * Statistics data is displayed (if available)
        """
        pass

    def test_004_navigate_to_console_and_observe_the_leaguetable_response_eg_httpsdf_api_gw_com_testladbrokescoralcomsdmstatsleaguetable3082api_keycom5856e59a2d264202be349165d8c59026(self):
        """
        DESCRIPTION: Navigate to console and observe the 'leaguetable' response (e.g. https://df-api-gw-com-test.ladbrokescoral.com/sdm/stats/leaguetable/3082/?api-key=COM5856E59A2D264202BE349165D8C59026)
        EXPECTED: * 'leaguetable' response with statistics is received
        EXPECTED: ![](index.php?/attachments/get/122180478)
        """
        pass

    def test_005_click_the_x_close_button(self):
        """
        DESCRIPTION: Click the 'x' close button
        EXPECTED: * League Link popup is closed
        """
        pass
