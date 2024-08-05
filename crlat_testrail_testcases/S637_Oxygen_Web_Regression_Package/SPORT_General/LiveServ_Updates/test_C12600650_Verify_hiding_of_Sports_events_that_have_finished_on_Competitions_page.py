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
class Test_C12600650_Verify_hiding_of_Sports_events_that_have_finished_on_Competitions_page(Common):
    """
    TR_ID: C12600650
    NAME: Verify hiding of <Sports> events that have finished on Competitions page
    DESCRIPTION: This test case verifies hiding of <Sports> events that have finished on Competitions page
    PRECONDITIONS: 1. LiveServer is available for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 3. To verify 'Displayed' and 'Result_conf' attributes values check Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 4. Use http://backoffice-tst2.coral.co.uk/ti/ for triggering events undisplaying or setting results
    PRECONDITIONS: *NOTE:* *LiveServe pushes with updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True

    def test_001_navigate_to_competitions_page(self):
        """
        DESCRIPTION: Navigate to 'Competitions' page
        EXPECTED: 'Competitions' page is opened
        """
        pass

    def test_002_verify_that_event_is_present(self):
        """
        DESCRIPTION: Verify that event is present
        EXPECTED: Event is displaying
        """
        pass

    def test_003_undisplay_event_from_the_current_page(self):
        """
        DESCRIPTION: Undisplay event from the current page
        EXPECTED: * [displayed:"N"] attribute is received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        pass

    def test_004_set_results_for_another_event_from_the_current_page(self):
        """
        DESCRIPTION: Set results for another event from the current page
        EXPECTED: * [displayed:"N"] or [result_conf:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        EXPECTED: * Whole type section disappears on front end if it contains only one event
        """
        pass
