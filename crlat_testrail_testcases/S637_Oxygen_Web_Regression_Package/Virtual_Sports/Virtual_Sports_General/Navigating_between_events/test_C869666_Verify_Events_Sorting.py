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
class Test_C869666_Verify_Events_Sorting(Common):
    """
    TR_ID: C869666
    NAME: Verify Events Sorting
    DESCRIPTION: This test case verifies that the list of events is sorted by start time by ascending (Start time incerases the each next event)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_check_start_time_of_the_list_of_events_in_the_event_selector_and_also_next_to_event_name(self):
        """
        DESCRIPTION: Check start time of the list of events (in the event selector and also next to event name)
        EXPECTED: Events are sorted by start time in ascending order
        """
        pass

    def test_002_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
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
