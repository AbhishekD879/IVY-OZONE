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
class Test_C146857_Verify_Football_Half_Time_Displaying_in_My_Bets_section(Common):
    """
    TR_ID: C146857
    NAME: Verify Football Half Time Displaying in 'My Bets' section
    DESCRIPTION: This test case verifies Half Time Displaying on 'Cash Out', 'Open Bets' and 'Bet History' tabs
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed bets on **Football** matches (Singles and Multiple bets) where Cash Out offer is available;
    PRECONDITIONS: *   Event is started
    PRECONDITIONS: In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **periodCode** with an attribute **state="S"** (this means that the clock is "stopped")
    PRECONDITIONS: *   **periodCode="HALF_TIME"** - Half time in a match/game
    PRECONDITIONS: NOTE: UAT assistance is needed in order to generate half time for BIP event.
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_002_verify_single_selection_with_half_time_available(self):
        """
        DESCRIPTION: Verify Single selection with Half Time available
        EXPECTED: Single selection with Half Time is shown
        """
        pass

    def test_003_verify_halftime_displaying(self):
        """
        DESCRIPTION: Verify Half Time displaying
        EXPECTED: **HT** label is shown near Team Names (on the right side)
        """
        pass

    def test_004_verify_half_time_correctness(self):
        """
        DESCRIPTION: Verify Half Time correctness
        EXPECTED: Event with attributes **state="S"** and **periodCode="HALF_TIME"** is shown
        """
        pass

    def test_005_verify_multiple_selection_withhalf_time_available(self):
        """
        DESCRIPTION: Verify Multiple selection with Half Time available
        EXPECTED: Multiple selection with Half Time is shown
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps №3-4
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_6_for_cash_out_tab_open_bets_tab_bet_history_tab_my_bets_tab_within_event_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: * 'Cash Out' tab
        DESCRIPTION: * 'Open Bets' tab
        DESCRIPTION: * 'Bet History' tab
        DESCRIPTION: * 'My Bets' tab within Event Details page
        EXPECTED: 
        """
        pass
