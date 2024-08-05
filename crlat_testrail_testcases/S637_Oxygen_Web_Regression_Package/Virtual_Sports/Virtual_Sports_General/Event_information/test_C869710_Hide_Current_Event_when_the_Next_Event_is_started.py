import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869710_Hide_Current_Event_when_the_Next_Event_is_started(Common):
    """
    TR_ID: C869710
    NAME: Hide Current Event when the Next Event is started
    DESCRIPTION: This test case verifies that the next event is shown in the application when the previous one is NOT finished.
    PRECONDITIONS: This test case can be verified only when events are not settled on the server side (isResulted and isFinished attributes are not set). If events are settled then test case will be Blocked
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_wait_untill_the_next_event_starts_isstarted__true(self):
        """
        DESCRIPTION: Wait untill the next event starts (isStarted = true)
        EXPECTED: * 'Live' label appears above the sport icon in the carousel [Till 102.1]
        EXPECTED: * "LIVE" label is displayed next to the event start time in the first accordion [Till 102.1]
        EXPECTED: * Video stream is (or can be) activated
        """
        pass

    def test_002_verify_the_moment_when_the_next_event_after_current_one_is_started(self):
        """
        DESCRIPTION: Verify the moment when the next event after current one is started
        EXPECTED: Page is refreshed to show the next event at the moment when **the next event is started**, however previous one was not yet finished:
        EXPECTED: *   Current event is no more displayed
        EXPECTED: *   Next event is shown
        EXPECTED: *   'Live' labels are not shown anymore [Till 102.1]
        EXPECTED: *   'Price/Odds' buttons become enabled
        """
        pass

    def test_003_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following virtual sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis,
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass
