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
class Test_C60089716_Verify_GA_tracking_of_In_Line_Market_Stats_Links(Common):
    """
    TR_ID: C60089716
    NAME: Verify GA tracking of In-Line Market Stats Links
    DESCRIPTION: This test case verifies GA tracking when user clicks on "Show Statistics" link on Football EDP
    PRECONDITIONS: * Master Toggle for "Statistics Links" should be enabled in System Configuration (CMS -> System Configuration -> Config -> StatisticsLinks)
    PRECONDITIONS: *  Market Link is configured at least for one Market (CMS -> Statistics Links -> Market Links)
    PRECONDITIONS: (Full list of Markets Name, templateMarketName, tabKey, and overlay key are attached in the Story https://jira.egalacoral.com/browse/BMA-56388)
    """
    keep_browser_open = True

    def test_001_navigate_to_any_football_edp_from_preconditions_click_on_show_statistics_link_and_check_datalayer__object(self):
        """
        DESCRIPTION: Navigate to any Football EDP from preconditions, click on "Show Statistics" link and check dataLayer  object
        EXPECTED: Following event is present:
        EXPECTED: event: “trackEvent”,
        EXPECTED: eventCategory: “in-line stats”
        EXPECTED: eventAction: “view statistics”
        EXPECTED: eventLabel: “display”, // i.e. “both teams to score”, “clean sheet” or “to win to nil”
        EXPECTED: sport: <OpenBet Category ID>, // i.e. “16”
        EXPECTED: competitionID: <OpenBet Type ID>, // i.e. ”3082”
        EXPECTED: eventID: <OpenBet EventID>, // i.e. “231316986”
        EXPECTED: eventName: <Open Bet Event> // i.e. “Middlesbrough FC v Coventry City”
        EXPECTED: ![](index.php?/attachments/get/122251553)
        """
        pass
