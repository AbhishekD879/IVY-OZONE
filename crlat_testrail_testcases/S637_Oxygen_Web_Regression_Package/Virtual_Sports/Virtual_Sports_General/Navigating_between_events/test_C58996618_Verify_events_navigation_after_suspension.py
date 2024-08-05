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
class Test_C58996618_Verify_events_navigation_after_suspension(Common):
    """
    TR_ID: C58996618
    NAME: Verify events navigation after suspension
    DESCRIPTION: This test case verifies events navigation after suspension
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_wait_until_the_first_event_go_live(self):
        """
        DESCRIPTION: Wait until the **first** event go Live
        EXPECTED: - User should be moved to the **next** available race card/EDP
        EXPECTED: - Selections for **first** event become suspended for betting
        """
        pass

    def test_002_open_the_last_event_which_is_live_and_wait_till_it_finish(self):
        """
        DESCRIPTION: Open the **last** event which is **Live** and wait till it finish
        EXPECTED: - User should be on the same event until page refresh
        EXPECTED: - Child should also be removed when the event drops off
        EXPECTED: - User navigated to the other child sport/Other parent sport
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
