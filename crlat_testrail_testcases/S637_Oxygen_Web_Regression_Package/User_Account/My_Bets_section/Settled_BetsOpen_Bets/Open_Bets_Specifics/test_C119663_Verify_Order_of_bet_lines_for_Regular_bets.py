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
class Test_C119663_Verify_Order_of_bet_lines_for_Regular_bets(Common):
    """
    TR_ID: C119663
    NAME: Verify Order of bet lines for Regular bets
    DESCRIPTION: This test case verifies order of  'Regular' bet lines on 'Open Bets' tab when the user is logged in
    DESCRIPTION: AUTOTEST [C527795]
    DESCRIPTION: AUTOTEST [C1501850]
    DESCRIPTION: AUTOTEST [C1501666]
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * Place simultaneous a few bets (multiples and singles) (in order to get the same Bet Placement Time) including YourCall bets
    PRECONDITIONS: * Place a few bets (multiples and singles) at different time (in order to get bet lines with different Bet Placement Time)
    PRECONDITIONS: * Place simultaneously a few bets on the same event but different markets/selections (in order to get the same Bet Placement Time and Event Start Time)
    PRECONDITIONS: Note:
    PRECONDITIONS: Bets from YourCall Markets are displayed within Regular bets Tab
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_open_bets_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Open bets' tab is opened
        EXPECTED: * 'Regular' sort filter is selected by default
        """
        pass

    def test_003_verify_order_of_bets_within_the_same_date_panel(self):
        """
        DESCRIPTION: Verify order of bets within the same date panel
        EXPECTED: All bets are ordered chronologically by bet placement time (the most recent first)
        """
        pass

    def test_004_verify_order_of_bets_with_the_same_bet_placement_time(self):
        """
        DESCRIPTION: Verify order of bets with the same bet placement time
        EXPECTED: *   Bet lines are ordered by Event Start Time (with the earliest start time first)
        EXPECTED: *   In case of the same Event Start Time - in the order they come back from betplacement API (accountHistory response)
        """
        pass
