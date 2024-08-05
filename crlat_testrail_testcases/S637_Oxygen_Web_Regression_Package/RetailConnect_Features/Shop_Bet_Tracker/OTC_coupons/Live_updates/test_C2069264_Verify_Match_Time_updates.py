import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2069264_Verify_Match_Time_updates(Common):
    """
    TR_ID: C2069264
    NAME: Verify Match Time updates
    DESCRIPTION: This test case verifies Match Time Updates within coupon
    DESCRIPTION: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    PRECONDITIONS: *   Valid Cash Out Coupon Code should be generated with Live Scores available (support is needed from RCOMB team)
    PRECONDITIONS: *   Commentary data is available only for started events
    PRECONDITIONS: *   To find all details related to the coupon open browser console (F12) -> Network -> request 'coupon?id=<coupon code>' -> Preview
    PRECONDITIONS: *   To find details about live scores in Preview tab of 'coupon?id=<coupon code>' request expand the following elements : bet -> leg -> sportsLeg -> legPart -> eventParticipants/eventPeriod
    PRECONDITIONS: In order to get events with Scorers use link, where XXX - event id:
    PRECONDITIONS: http://backoffice-tst2.coralbip.co.uk/openbet-ssviewer/Commentary/2.15/CommentaryForEvent/XXX
    PRECONDITIONS: Look at the attributes to know event period:
    PRECONDITIONS: *   **offset** - match time in seconds on periodCode="FIRST_HALF/SECOND_HALF" level
    PRECONDITIONS: *   **periodCode="FIRST_HALF"** - First half of a match, state="S" (this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="SECOND_HALF"** - Second half of a match, state="R" (this means that the clock is "running")
    PRECONDITIONS: *   **periodCode="HALF_TIME"** - Half time in a match, state="S"
    PRECONDITIONS: *   **periodCode="FINISH"** - End of a match, **state="S"**
    PRECONDITIONS: * All live updates are coming through WebSockets
    PRECONDITIONS: ** Events score/time can be managed in ATS Amelco **
    PRECONDITIONS: **Run test case simultaneously on both 'Shop Bet Tracker' page and 'My Bets' ->'In-Shop Bets' sub-tub**
    """
    keep_browser_open = True

    def test_001__load_sportbook_app_log_in_chose_connect_from_header_ribbon_select_shop_bet_tracker(self):
        """
        DESCRIPTION: * Load Sportbook App
        DESCRIPTION: * Log in
        DESCRIPTION: * Chose 'Connect' from header ribbon
        DESCRIPTION: * Select 'Shop Bet Tracker'
        EXPECTED: Bet Tracker page is opened
        """
        pass

    def test_002_submit_valid_cash_out_code_which_containspre_play_event(self):
        """
        DESCRIPTION: Submit valid Cash Out Code which contains pre-play event
        EXPECTED: * Cash Out Code is submitted successfully
        EXPECTED: * Cash Out Coupon is shown to the user expanded by default
        EXPECTED: * Match start time/date is displayed under ball icon
        """
        pass

    def test_003__verify_start_time_correctness(self):
        """
        DESCRIPTION: * Verify Start Time correctness
        EXPECTED: * Event start time corresponds to '**startTime**' attribute
        EXPECTED: * Start time is shown below the icon in the following format in user's time zone:
        EXPECTED: * for today events - 'Today HH:MM AM/PM'
        EXPECTED: * for events that take place within the next seven days - '<Name of the day> HH:MM AM/PM' (e.g. Tue 4:00 PM)
        EXPECTED: * for future events beyond the next seven days - '<Day> <Month> HH:MM AM/PM' (e.g. 20 May 4:00 PM)
        """
        pass

    def test_004_trigger_event_kick_off(self):
        """
        DESCRIPTION: Trigger event kick-off
        EXPECTED: *   Event is started
        EXPECTED: *   Match time is shown below the Sport icon instead of Start Time in format: **MM** (minutes only)
        EXPECTED: * Match Time corresponds to an attribute **offset **on active periodCode level:
        EXPECTED: periodCode="FIRST_HALF" (if it is first half now) or periodCode="SECOND_HALF" (if it is first half now)
        EXPECTED: * offset in seconds **/ 60 = ****offset **in minutes (only value before comma is taken into consideration)
        """
        pass

    def test_005_change_event_period_to_half_time(self):
        """
        DESCRIPTION: Change event period to Half Time
        EXPECTED: **'HT' **label is shown instead of Match Time
        """
        pass

    def test_006_start_event_again___event_is_moved_to_second_half_period(self):
        """
        DESCRIPTION: Start event again -> event is moved to Second half period
        EXPECTED: * 'HT' label is changed to Match Time that starts from 45
        """
        pass

    def test_007_finish_event_change_event_period_to_normal_time_end___game_is_finished(self):
        """
        DESCRIPTION: Finish event: change event period to Normal time end -> Game is finished
        EXPECTED: * 'FT' label is shown instead of Match Time for finished events
        EXPECTED: * Event information with results is available till event is present in SS
        """
        pass

    def test_008_go_to_my_bets__in_shop_bets_sub_tub__repeat_steps_3_7(self):
        """
        DESCRIPTION: Go to 'My Bets' ->'In-Shop Bets' sub-tub ->
        DESCRIPTION: repeat steps #3-7
        EXPECTED: 
        """
        pass
