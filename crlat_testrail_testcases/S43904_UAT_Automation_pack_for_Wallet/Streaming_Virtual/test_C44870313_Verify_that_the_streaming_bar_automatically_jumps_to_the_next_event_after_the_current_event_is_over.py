import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C44870313_Verify_that_the_streaming_bar_automatically_jumps_to_the_next_event_after_the_current_event_is_over(Common):
    """
    TR_ID: C44870313
    NAME: Verify that the streaming bar automatically jumps to the next event after the current event is over.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_virtuals_and_to_grand_nationals_verify(self):
        """
        DESCRIPTION: Navigate to Virtuals and to Grand Nationals. Verify.
        EXPECTED: The live stream for Grand Nationals is playing properly/smoothly.
        """
        pass

    def test_002_verify_the_streaming_bar_once_the_current_event_is_over(self):
        """
        DESCRIPTION: Verify the streaming bar once the current event is over.
        EXPECTED: The streaming bar automatically jumps to the next event once the current event is over.
        """
        pass

    def test_003_place_a_bet_and_verify(self):
        """
        DESCRIPTION: Place a bet and verify.
        EXPECTED: Bet is placed successfully.
        """
        pass

    def test_004_perform_steps_1_3_for_the_following_virtuals_1_hr_jumps2_greyhounds3_horse_racing4_football5_motorsports(self):
        """
        DESCRIPTION: Perform steps 1-3 for the following virtuals:-
        DESCRIPTION: 1. HR Jumps
        DESCRIPTION: 2. Greyhounds
        DESCRIPTION: 3. Horse Racing
        DESCRIPTION: 4. Football
        DESCRIPTION: 5. Motorsports
        EXPECTED: The result is same as mentioned in steps 1-3
        """
        pass
