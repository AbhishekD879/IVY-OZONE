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
class Test_C60089718_Verify_GA_tracking_of_In_Line_League_Tables_button_in_Football_Coupons(Common):
    """
    TR_ID: C60089718
    NAME: Verify GA tracking of In-Line League Tables button in Football Coupons
    DESCRIPTION: This test case verifies GA tracking when user clicks on "League Tables" button in Football Coupons page
    PRECONDITIONS: * Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: * Statistic Link is configured at least for one Coupon and one League (CMS -> Statistics Links -> League Links) (e.g. "English Premier League")
    """
    keep_browser_open = True

    def test_001_navigate_to_any_football_coupon_page_from_preconditions_click_on_league_tables_link_and_check_datalayer_object(self):
        """
        DESCRIPTION: Navigate to any Football Coupon page from preconditions, click on "League Tables" link and check dataLayer object
        EXPECTED: Following event is present:
        EXPECTED: event: “trackEvent”,
        EXPECTED: eventCategory: “in-line stats”,
        EXPECTED: eventAction: “league table”,
        EXPECTED: eventLabel: “display”, // i.e. “premier league” or “championship”
        EXPECTED: sport: <OpenBet Category ID>, // i.e. “16”
        EXPECTED: competitionID: <OpenBet Type ID>, // i.e. ”3082”
        EXPECTED: ![](index.php?/attachments/get/122251554)
        """
        pass
