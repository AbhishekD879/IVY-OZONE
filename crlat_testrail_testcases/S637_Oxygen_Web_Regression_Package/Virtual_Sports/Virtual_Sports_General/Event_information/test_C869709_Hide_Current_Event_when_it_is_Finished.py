import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869709_Hide_Current_Event_when_it_is_Finished(Common):
    """
    TR_ID: C869709
    NAME: Hide Current Event when it is Finished
    DESCRIPTION: This test case verifies that the next event is shown in the application when previous one is finished
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_wait_until_the_next_event_is_started_isstarted__true(self):
        """
        DESCRIPTION: Wait until the next event is started (isStarted = true)
        EXPECTED: * 'Live' label appears above the event icon [Till 102.1]
        EXPECTED: * "LIVE" label is shown next to event start date in the first accordion [Till 102.1]
        EXPECTED: * Video stream is (or can be) activated
        EXPECTED: * Event is suspended for betting
        """
        pass

    def test_002_wait_until_the_event_isfinished_isfinished__true(self):
        """
        DESCRIPTION: Wait until the event is finished (isFinished = true)
        EXPECTED: Page is refreshed in **15 seconds** after isFinished attribute is set for the event:
        EXPECTED: *   Current event is no more displayed
        EXPECTED: *   Next event is shown
        EXPECTED: *   'Live' labels are not shown anymore [Till 102.1]
        EXPECTED: *   'Price/Odds' buttons of the next event are enabled
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
