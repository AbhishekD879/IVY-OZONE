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
class Test_C869668_Verify_Automatical_Data_Retrieving(Common):
    """
    TR_ID: C869668
    NAME: Verify Automatical Data Retrieving
    DESCRIPTION: This test case verifies that data are updated automatically each 1 hour and new events appear.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_navigate_to_the_last_event(self):
        """
        DESCRIPTION: Navigate to the last event
        EXPECTED: 
        """
        pass

    def test_002_check_event_name_start_timestart_date_for_the_last_event(self):
        """
        DESCRIPTION: Check event name, start time/start date for the last event
        EXPECTED: 
        """
        pass

    def test_003_wait_1_hour(self):
        """
        DESCRIPTION: Wait 1 hour
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_the_last_event_and_check_event_name_start_timestart_date(self):
        """
        DESCRIPTION: Navigate to the last event and check event name, start time/start date
        EXPECTED: New events appear for the next 1 hour
        """
        pass

    def test_005_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
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
