import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C146858_Verify_Football_Match_Time_Half_Time_Updates_in_My_Bets_section(Common):
    """
    TR_ID: C146858
    NAME: Verify Football  Match Time/Half Time Updates in 'My Bets' section
    DESCRIPTION: This test case verifies Match Time/Half Time Updates on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Football** matches (Singles and Multiples) where Cash Out offer is available;
    PRECONDITIONS: *   Event is started
    PRECONDITIONS: In order to get events with Scorers use link:
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

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_selection_with_availablematch_time_for_first_half(self):
        """
        DESCRIPTION: Verify Single selection with available Match Time for First Half
        EXPECTED: Single selection with available Match Time for First Half is shown
        """
        pass

    def test_003_verify_match_time(self):
        """
        DESCRIPTION: Verify match time
        EXPECTED: *   Time is running in real time
        EXPECTED: *   Match Time corresponds to an attribute **offset** on periodCode="FIRST_HALF" level
        """
        pass

    def test_004_wait_till_the_end_of_first_half_and_check_timer(self):
        """
        DESCRIPTION: Wait till the end of First Half and check timer
        EXPECTED: Timer is replaced with 'HT' label
        """
        pass

    def test_005_wait_till_the_end_of_half_time_and_check_ht_label(self):
        """
        DESCRIPTION: Wait till the end of Half Time and check 'HT' label
        EXPECTED: 'HT' label is replaced with timer
        """
        pass

    def test_006_verify_match_time(self):
        """
        DESCRIPTION: Verify match time
        EXPECTED: *   Time is running in real time
        EXPECTED: *   Match Time corresponds to an attribute **offset** on periodCode="SECOND_HALF" level
        """
        pass

    def test_007_verify_match_time_before_bip_page_is_opened(self):
        """
        DESCRIPTION: Verify Match Time before BIP page is opened
        EXPECTED: If page was opened, user navigated to other page and returned to verified event - updated timer will be shown there with correct Match Time or 'HT' label (if it is Half Time now)
        """
        pass

    def test_008_verify_match_time_after_turned_off_phone_to_sleep_mode(self):
        """
        DESCRIPTION: Verify Match Time after turned off phone to sleep mode
        EXPECTED: If phone was turned off to sleep mode and turned on again, updated timer will be shown there with correct Match Time or 'HT' label (if it is Half Time now)
        """
        pass

    def test_009_verify_multiple_selection_with_availablematch_time(self):
        """
        DESCRIPTION: Verify Multiple selection with available Match Time
        EXPECTED: Multiple selection with available Match Time is shown
        """
        pass

    def test_010_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps №3-8
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_2_10_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-10 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
