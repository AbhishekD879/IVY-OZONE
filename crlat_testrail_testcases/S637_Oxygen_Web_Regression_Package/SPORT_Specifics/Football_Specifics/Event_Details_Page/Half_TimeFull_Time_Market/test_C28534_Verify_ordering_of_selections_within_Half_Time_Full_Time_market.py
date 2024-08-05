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
class Test_C28534_Verify_ordering_of_selections_within_Half_Time_Full_Time_market(Common):
    """
    TR_ID: C28534
    NAME: Verify ordering of selections within 'Half Time/Full Time' market
    DESCRIPTION: This test case verifies ordering of selections within 'Half Time/Full Time' market
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_verify_order_within_market_section(self):
        """
        DESCRIPTION: Verify order within market section
        EXPECTED: Section is ordered in following way:
        EXPECTED: * <Home/Home>
        EXPECTED: * < Home/Draw>
        EXPECTED: * <Home/Away>
        EXPECTED: * <Draw/Home>
        EXPECTED: * <Draw/Draw>
        EXPECTED: * <Draw/Away>
        EXPECTED: * <Away/Home>
        EXPECTED: * <Away/Draw>
        EXPECTED: * <Away/Away>
        """
        pass
