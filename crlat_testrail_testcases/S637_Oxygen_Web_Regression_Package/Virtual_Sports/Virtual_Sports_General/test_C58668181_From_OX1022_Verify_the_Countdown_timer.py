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
class Test_C58668181_From_OX1022_Verify_the_Countdown_timer(Common):
    """
    TR_ID: C58668181
    NAME: From [OX102.2] Verify the Countdown timer
    DESCRIPTION: This test case verifies the view of Countdown timer.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment.
    PRECONDITIONS: 2. Go to 'Virtual Sports'.
    """
    keep_browser_open = True

    def test_001_observe_event_which_will_start_after_30plus_seconds(self):
        """
        DESCRIPTION: Observe event which will start after 30+ seconds.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - Timer inside circle is counting down
        EXPECTED: - Circle is grey
        EXPECTED: ![](index.php?/attachments/get/105735340)
        """
        pass

    def test_002_observe_event_which_will_start_in_0_29_seconds(self):
        """
        DESCRIPTION: Observe event which will start in 0-29 seconds.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - Timer inside circle is counting down
        EXPECTED: - Circle turns blue
        EXPECTED: ![](index.php?/attachments/get/105735354)
        """
        pass

    def test_003_observe_event_which_already_started(self):
        """
        DESCRIPTION: Observe event which already started.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - The "LIVE" string is displayed inside instead of Timer
        EXPECTED: - Circle is blue
        EXPECTED: ![](index.php?/attachments/get/105735356)
        """
        pass

    def test_004_observe_event_which_will_start_after_60_minutes(self):
        """
        DESCRIPTION: Observe event which will start after 60 minutes.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - Timer inside circle is counting down
        EXPECTED: - Circle is grey
        EXPECTED: - The time is displayed with +60 value in the left part of the timer (e.g., "61:06").
        """
        pass
