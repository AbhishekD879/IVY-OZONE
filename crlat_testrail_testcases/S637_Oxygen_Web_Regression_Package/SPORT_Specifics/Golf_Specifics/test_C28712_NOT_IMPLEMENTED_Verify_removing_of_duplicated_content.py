import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28712_NOT_IMPLEMENTED_Verify_removing_of_duplicated_content(Common):
    """
    TR_ID: C28712
    NAME: NOT IMPLEMENTED: Verify removing of duplicated content
    DESCRIPTION: This test case verifies removing of duplicated content.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-12292: Golf - Rename Matches tab and remove duplicated content
    PRECONDITIONS: Use http://backoffice-tst2.coral.co.uk/ti/ for setting up the Golf events with appropriate markets.
    PRECONDITIONS: At event level neccessary to choose 'Sort' type. For event that contains 2/3 Balls markets you should to select MATCH in 'Sort' field but for event that contains other markets (NOT 2/3 Balls) you should chose TOURNAMENT in 'Sort' field.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_page(self):
        """
        DESCRIPTION: Load Oxygen page
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_golf_page(self):
        """
        DESCRIPTION: Go to 'Golf' page
        EXPECTED: *   Golf Landing Page is opened
        EXPECTED: *   2/3 Balls' -> 'Today' page is opened by default
        """
        pass

    def test_003_verify_list_of_markets(self):
        """
        DESCRIPTION: Verify list of markets
        EXPECTED: *   Enhanced Muiltiples section is displayed at the top of the page
        EXPECTED: *   Only ''2 Balls' and '3 Balls' markets are displayed on the '2/3 Balls' page
        EXPECTED: *   There are no markets that are not 2/3 Balls
        """
        pass

    def test_004_verify_list_of_event_in_the_23_balls_page(self):
        """
        DESCRIPTION: Verify list of event in the '2/3 Balls' page
        EXPECTED: *   Only events that have 'MATCH' value in 'Sort' field in OpenBet are displayed in the '2/3 Balls' page
        """
        pass
