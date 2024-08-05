import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C10940585_Football_BIP_events_Match_Time_Displaying(Common):
    """
    TR_ID: C10940585
    NAME: Football BIP events: Match Time Displaying
    DESCRIPTION: This test case verifies match time displaying and updating of Football BIP event in Featured module by Football EventID.
    PRECONDITIONS: 1. Module by Football EventId is created in CMS and contains event
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: - In order to see match time Football event should be BIP event
    PRECONDITIONS: - In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **offset **- match time in seconds on periodCode="FIRST\_HALF/SECOND\_HALF" level
    PRECONDITIONS: *   **periodCode="FIRST_HALF" - **First half of a match/game, **state="S" **(this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="SECOND_HALF" - **Second half of a match/game, **state="R" **(this means that the clock is "running")
    PRECONDITIONS: *   **periodCode="HALF_TIME" - **Half time in a match/game, **state="S"**
    PRECONDITIONS: NOTE: UAT assistance is needed in order to generate match time for BIP event.
    PRECONDITIONS: **Match Time updates in real time based on subscription for Live Timer or if it is not available then devise's time should be user as Timer for updating Match Time.**
    """
    keep_browser_open = True

    def test_001_navigate_to_created_module_and_verify_football_event_with_match_time_available(self):
        """
        DESCRIPTION: Navigate to Created module and verify Football event with Match Time available
        EXPECTED: Event is shown
        """
        pass

    def test_002_verify_match_time_displaying(self):
        """
        DESCRIPTION: Verify Match Time displaying
        EXPECTED: Match time is shown below the Sport icon instead of Start Time in format:
        EXPECTED: **MM** (minutes only)
        """
        pass

    def test_003_verify_match_time_correctness(self):
        """
        DESCRIPTION: Verify Match Time correctness
        EXPECTED: *   Match Time corresponds to an attribute **offset **on active periodCode level:
        EXPECTED: periodCode="FIRST\_HALF" (if it is first half now) or periodCode="SECOND\_HALF" (if it is first half now)
        EXPECTED: *   **offset **in seconds **/ 60 = ****offset **in minutes (only value before comma is taken into consideration)
        """
        pass

    def test_004_verify_match_time(self):
        """
        DESCRIPTION: Verify match time
        EXPECTED: *   Time is running in real time
        EXPECTED: *   Match Time corresponds to an attribute **offset **on periodCode="FIRST_HALF" level
        """
        pass

    def test_005_wait_till_the_end_of_first_half_and_check_timer(self):
        """
        DESCRIPTION: Wait till the end of First Half and check timer
        EXPECTED: Timer is replaced with 'HT' label
        """
        pass

    def test_006_wait_till_the_end_of_half_time_and_check_ht_label(self):
        """
        DESCRIPTION: Wait till the end of Half Time and check 'HT' label
        EXPECTED: 'HT' label is replaced with timer
        """
        pass

    def test_007_verify_match_time(self):
        """
        DESCRIPTION: Verify match time
        EXPECTED: *   Time is running in real time
        EXPECTED: *   Match Time corresponds to an attribute **offset **on periodCode="SECOND_HALF" level
        """
        pass
