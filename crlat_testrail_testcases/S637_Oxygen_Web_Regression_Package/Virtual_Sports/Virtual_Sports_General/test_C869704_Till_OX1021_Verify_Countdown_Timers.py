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
class Test_C869704_Till_OX1021_Verify_Countdown_Timers(Common):
    """
    TR_ID: C869704
    NAME: [Till OX102.1] Verify Countdown Timers
    DESCRIPTION: This test case verifies video and event countdown timers
    PRECONDITIONS: Next Event starts more than 1 m 20 s
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_check_video_countdown_timer_if_the_event_starts_beyondthe_next_1m_20s(self):
        """
        DESCRIPTION: Check video countdown timer if the event starts BEYOND the next 1m 20s
        EXPECTED: Video countdown timer is shown in the middle of the video section:
        EXPECTED: 'Video starts in: HH:MM:SS'
        """
        pass

    def test_002_check_event_countdown_timer_if_the_event_startswithin_the_next_1m_20s(self):
        """
        DESCRIPTION: Check event countdown timer if the event starts WITHIN the next 1m 20s
        EXPECTED: Event countdown is shown before the event name in MM:SS format
        """
        pass

    def test_003_check_video_countdown_timer_correctness(self):
        """
        DESCRIPTION: Check video countdown timer correctness
        EXPECTED: Countdown timer is reflected correctly according to the time when video starts
        """
        pass

    def test_004_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Repeat this test case for the following Virtual Sports:
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
