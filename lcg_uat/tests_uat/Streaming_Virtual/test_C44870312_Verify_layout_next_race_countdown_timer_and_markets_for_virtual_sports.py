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
class Test_C44870312_Verify_layout_next_race_countdown_timer_and_markets_for_virtual_sports(Common):
    """
    TR_ID: C44870312
    NAME: Verify layout,  next race countdown timer and markets for virtual sports
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_virtuals_and_verify_the_layout(self):
        """
        DESCRIPTION: Navigate to Virtuals and verify the layout.
        EXPECTED: 1. A sports carousel consisting of all the virtual sports with names and their corresponding icons is displayed. Either the 'LIVE' label or a countdown timer is displayed besides the sport icon (depending on the time remaining for the next event to start). The sport icon, name and LIVE label/countdown timer are displayed in yellow colour if it is selected, else in white colour.
        EXPECTED: 2. The event header consisting of the event venue (on the left) is displayed below the sports carousel with date and time of the current/next event (on the right). If current event is playing, then the date is displayed with LIVE label. If the next event is about to start, then the date and time of the next event is displayed.
        EXPECTED: 3. The live stream window is displayed.
        EXPECTED: 4. The event timings are displayed in the carousel below the live stream window. The user can scroll and select any of the timings and navigate to the event details page of that particular event.
        EXPECTED: 5. The markets with selections are displayed by default for the selected event (in the event timings carousel).
        """
        pass

    def test_002_compare_the_countdown_timer_in_the_live_stream_window_and_on_the_sports_carousel_for_the_next_racematch_available_when_the_next_race_is_starting_in_a_minute_verify(self):
        """
        DESCRIPTION: Compare the countdown timer in the live stream window and on the sports carousel for the next race/match (available when the next race is starting in a minute). Verify.
        EXPECTED: The timer in the live stream window and on the sports carousel are same/in sync. Note:- difference up to 10 seconds is acceptable.
        """
        pass

    def test_003_perform_step_2_for_the_following_sports_1_grand_national2_horse_racing3_hr_jumps4_greyhounds5_football6_motorsports(self):
        """
        DESCRIPTION: Perform step 2 for the following sports:-
        DESCRIPTION: 1. Grand National
        DESCRIPTION: 2. Horse Racing
        DESCRIPTION: 3. HR Jumps
        DESCRIPTION: 4. Greyhounds
        DESCRIPTION: 5. Football
        DESCRIPTION: 6. Motorsports
        EXPECTED: The expected result is as mentioned in step 2.
        """
        pass

    def test_004_verify_the_markets_available_for_the_following_sports_1_grand_national2_horse_racing3_hr_jumps4_greyhounds5_greyhounds6football7_motorsports(self):
        """
        DESCRIPTION: Verify the markets available for the following sports:-
        DESCRIPTION: 1. Grand National
        DESCRIPTION: 2. Horse Racing
        DESCRIPTION: 3. HR Jumps
        DESCRIPTION: 4. Greyhounds
        DESCRIPTION: 5. Greyhounds
        DESCRIPTION: 6.Football
        DESCRIPTION: 7. Motorsports
        EXPECTED: 1. The markets Win/Each way, Forecast and Tricast are available for all the races.
        EXPECTED: 2. Markets such as Match betting, Correct score etc are available for Football.
        """
        pass
