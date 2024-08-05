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
class Test_C28475_Verify_events_that_passed_Suspension_Time(Common):
    """
    TR_ID: C28475
    NAME: Verify events that passed "Suspension Time"
    DESCRIPTION: This test case verifies events removing from the <Sport> Event Details Page if they passed "Suspension Time"
    DESCRIPTION: **Story tickets:**
    DESCRIPTION: *   BMA-6527 As a TA I want to improve the caching efficiency of Football SiteServer data retrieval
    DESCRIPTION: *   BMA-7859
    DESCRIPTION: Note: looks like test case is not updated and milliseconds should not be rounded to the nearest '0/30' according to the comment in this bug:
    DESCRIPTION: https://jira.egalacoral.com/browse/BMA-50477
    PRECONDITIONS: To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Check "suspendAtTime="YYYY-MM-DDThh:mm:ssZ"" attribute to see the time, when the event should be removed from <Sport> Event Details Page
    PRECONDITIONS: Check **event.suspendAtTime** simple filter in **Networks **
    PRECONDITIONS: The **event.suspendAtTime** simple filter should simply be "2016-01-26T08:26:00.000Z" or "2016-01-26T08:26:30.000Z"
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:18.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:00.000
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:48.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:30.000
    PRECONDITIONS: The **event.suspendAtTime** simple filter should simply be "2016-01-26T08:26:10.000Z" and NOT "2016-01-26T08:26:22.967Z"
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Go to <Sport> Landing page
        EXPECTED: Landing page is opened representing available events
        """
        pass

    def test_003_go_to_sport_event_details_page(self):
        """
        DESCRIPTION: Go to <Sport> Event Details Page
        EXPECTED: <Sport> Event Details Page is opened with available markets
        """
        pass

    def test_004_checkeventsuspendattimesimple_filter_innetworksin_console(self):
        """
        DESCRIPTION: Check **event.suspendAtTime** simple filter in **Networks **(in Console)
        EXPECTED: The event.suspendAtTime simple filter should simply contain '00.000' seconds and milliseconds or '30.000' seconds and milliseconds
        EXPECTED: For example:
        EXPECTED: "2016-01-26T08:26:00.000Z" and **NOT **"2016-01-26T08:26:22.967Z"
        EXPECTED: or
        EXPECTED: "2016-01-26T08:26:30.000Z" and **NOT **"2016-01-26T08:26:22.967Z"
        """
        pass

    def test_005_check_ss_response_for_verified_event(self):
        """
        DESCRIPTION: Check SS response for verified event
        EXPECTED: **"suspendAtTime="YYYY-MM-DDThh:mm:ssZ""**** **attribute is present showing the time when event should be removed from the Details Page
        """
        pass

    def test_006_wait_until_time_ofsuspendattimepassed___refresh_details_page(self):
        """
        DESCRIPTION: Wait until time of **"suspendAtTime" **passed -> Refresh Details Page
        EXPECTED: 'No markets are currently available for this event' message is shown on the page and markets are not shown anymore.
        EXPECTED: Event is not shown on Football landing page.
        """
        pass
