import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C146856_To_editVerify_Match_Time_Displaying_in_My_Bets_section(Common):
    """
    TR_ID: C146856
    NAME: [To-edit]Verify Match Time Displaying in 'My Bets' section
    DESCRIPTION: [To-Edit] - needs to be edited according to all changes with Vanilla
    DESCRIPTION: This test case verifies Match Time Displaying on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Football** matches (Singles and Multiple bets) where Cash Out offer is available;
    PRECONDITIONS: In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **offset **- match time in seconds on periodCode="FIRST\_HALF/SECOND\_HALF" level
    PRECONDITIONS: *   **periodCode="FIRST_HALF" - **First half of a match/game, **state="S" **(this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="SECOND_HALF" - **Second half of a match/game, **state="R" **(this means that the clock is "running")
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_selection_withmatch_time_available(self):
        """
        DESCRIPTION: Verify Single selection with Match Time available
        EXPECTED: 
        """
        pass

    def test_003_verify_match_time_displaying(self):
        """
        DESCRIPTION: Verify Match Time displaying
        EXPECTED: Match time is shown near Team Names (on the right side) in format **MM:SS**
        """
        pass

    def test_004_verify_match_time_correctness(self):
        """
        DESCRIPTION: Verify Match Time correctness
        EXPECTED: *   Match Time corresponds to an attribute **offset** on active periodCode level:
        EXPECTED: periodCode="FIRST\_HALF" (if it is first half now) or periodCode="SECOND\_HALF" (if it is first half now)
        EXPECTED: *   **offset** in seconds/ 60 = **offset** in minutes (only value before comma is taken into consideration)
        """
        pass

    def test_005_verify_multiple_selection_with_match_time_available(self):
        """
        DESCRIPTION: Verify Multiple selection with Match Time available
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_3_4_for_multiples(self):
        """
        DESCRIPTION: Repeat steps №3-4 for Multiples
        EXPECTED: 
        """
        pass

    def test_007_verify_single_selection_which_doesnt_have_match_time_available(self):
        """
        DESCRIPTION: Verify Single selection which doesn't have Match Time available
        EXPECTED: * Badge with 'LIVE' label is shown near Team Names (on the right side)
        EXPECTED: * Match Time is not displayed
        """
        pass

    def test_008_repeat_step_7_for_multiples(self):
        """
        DESCRIPTION: Repeat step №7 for Multiples
        EXPECTED: 
        """
        pass

    def test_009_verify_start_time_displaying_for_upcoming_events(self):
        """
        DESCRIPTION: Verify Start Time displaying for Upcoming events
        EXPECTED: Start Time is shown near Team Names (on the right side)
        """
        pass

    def test_010_verify_start_time_correctness(self):
        """
        DESCRIPTION: Verify Start Time correctness
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   Event Start Time is shown below Sport icon
        EXPECTED: *   Date format is **DD MM** (e.g. 23 Feb) for future events and **12 hours AM/PM** (e.g. 7:00 AM) for today events
        """
        pass

    def test_011_repeat_9_10_steps_for_upcoming_multiple_selection(self):
        """
        DESCRIPTION: Repeat №9-10 steps for Upcoming Multiple selection
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_11_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-11 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
