import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28800_Verify_events_that_passed_Suspension_Time(Common):
    """
    TR_ID: C28800
    NAME: Verify events that passed "Suspension Time"
    DESCRIPTION: This test case verifies events removing from the <Race> Landing Page if they passed "Suspension Time"
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-6526 As a TA I want to improve the caching efficiency of Horse Racing SiteServer data retrieval
    DESCRIPTION: *   BMA-7859
    DESCRIPTION: Note: According to the comment https://jira.egalacoral.com/browse/BMA-50477 miliseconds should not be rounded as described below
    PRECONDITIONS: To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Check "suspendAtTime="YYYY-MM-DDThh:mm:ssZ"" attribute to see the time, when the event should be removed from <Race> Landing Page
    PRECONDITIONS: Check **event.suspendAtTime** simple filter in **Networks **
    PRECONDITIONS: The **event.suspendAtTime** simple filter should simply be "2016-01-26T08:26:00.000Z" or "2016-01-26T08:26:30.000Z"
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:18.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:00.000
    PRECONDITIONS: If the current timestamp is: 2016-04-03 05T22:20:48.000 then the event.suspendAtTime simple filter should be: 2016-04-03 05T22:20:30.000
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_race_landing_page(self):
        """
        DESCRIPTION: Go to <Race> Landing page
        EXPECTED: Landing page is opened representing available events
        """
        pass

    def test_003_checkeventsuspendattimesimple_filter_innetworksin_console(self):
        """
        DESCRIPTION: Check **event.suspendAtTime** simple filter in **Networks **(in Console)
        EXPECTED: The event.suspendAtTime simple filter should simply contain '00.000' seconds and milliseconds or '30.000' seconds and milliseconds
        EXPECTED: For example:
        EXPECTED: "2016-01-26T08:26:00.000Z" and **NOT **"2016-01-26T08:26:22.967Z"
        EXPECTED: or
        EXPECTED: "2016-01-26T08:26:30.000Z" and **NOT **"2016-01-26T08:26:22.967Z"
        """
        pass

    def test_004_pick_event_which_is_shown_on_landing_page_and_check_ss_response_for_it(self):
        """
        DESCRIPTION: Pick event which is shown on Landing Page and check SS response for it
        EXPECTED: **"suspendAtTime="YYYY-MM-DDThh:mm:ssZ""**** **attribute is present showing the time when event should be removed from the verified Landing Page
        """
        pass

    def test_005_wait_until_time_ofsuspendattimepassed___refresh_landing_page(self):
        """
        DESCRIPTION: Wait until time of **"suspendAtTime" **passed -> Refresh Landing page
        EXPECTED: Verified event is no more shown on  Landing Page
        """
        pass
