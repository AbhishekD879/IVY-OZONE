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
class Test_C29214_Verify_Bet_Details_of_Football_Jackpot_bets_on_Open_Bets(Common):
    """
    TR_ID: C29214
    NAME: Verify Bet Details of Football Jackpot bets on Open Bets
    DESCRIPTION: This test case verifies 'Open Bets' tab when user Logged In for 'Pools'
    DESCRIPTION: **Jira tickets:** BMA-3145, BMA-6231, BMA-17176, BMA-17175, BMA-17820, BMA-28178
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have Open Football Jackpot bets
    """
    keep_browser_open = True

    def test_001_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: *   'My Bets' page/'Bet Slip' widget is shown
        EXPECTED: *   'Open Bets' tab is shown next to 'Cash Out' tab
        """
        pass

    def test_002_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: * 'Regular' filter is selected by default
        EXPECTED: * User's open bets are shown (if available)
        """
        pass

    def test_003_select_pools_filter(self):
        """
        DESCRIPTION: Select 'Pools' filter
        EXPECTED: * 'Pools' filter is selected
        EXPECTED: * User's football jackpot open bets are shown
        EXPECTED: * All bets are ordered chronologically (most recent first)
        EXPECTED: * If there are more than 20 bets, they are loaded in portions of 20
        """
        pass

    def test_004_verify_bet_details_of_an_open_fj_bet(self):
        """
        DESCRIPTION: Verify bet details of an **Open** FJ bet
        EXPECTED: The following bet details are shown:
        EXPECTED: * **"FOOTBALL JACKPOT 15"** label in the section header
        EXPECTED: * All selections, which are included in the bet, one under another in the following format:
        EXPECTED: **<Selection name>**
        EXPECTED: <Event name> <event start date and time>
        EXPECTED: Example:
        EXPECTED: **Draw**
        EXPECTED: Barcelona v Levante Today, 6:00 PM
        EXPECTED: * If selection is resulted, there is a "✓" / "X" mark at the right side, indicating that the selection is won/lost
        EXPECTED: * Panel containing date of bet placement (e.g., **"24/02/2017"**) on the left and bet receipt number ( e.g., **"Bet Receipt O/12454738/0000184"**) on the right
        EXPECTED: * Stake in format "Stake <currency symbol> <number>, e.g.: **"Stake £10.00"**
        EXPECTED: * Number of lines and win lines in format "Lines <number> Win Lines <number>", e.g.: **"Lines 8 Win Lines 0"**
        """
        pass

    def test_005_result_a_fj_bet_so_that_it_becomes_won_and_check_of_the_bet_disappears_from_open_bets_tab(self):
        """
        DESCRIPTION: Result a FJ bet so that it becomes "WON" and check of the bet disappears from "Open Bets" tab
        EXPECTED: Bet with 'Won' status is NOT displayed in 'Open Bets' tab
        """
        pass

    def test_006_result_a_fj_bet_so_that_it_becomes_lost_and_check_of_the_bet_disappears_from_open_bets_tab(self):
        """
        DESCRIPTION: Result a FJ bet so that it becomes "LOST" and check of the bet disappears from "Open Bets" tab
        EXPECTED: Bet with 'LOST' status is NOT displayed in 'Open Bets' tab
        """
        pass

    def test_007_result_a_fj_bet_so_that_it_becomes_void_and_check_of_the_bet_disappears_from_open_bets_tab(self):
        """
        DESCRIPTION: Result a FJ bet so that it becomes "VOID" and check of the bet disappears from "Open Bets" tab
        EXPECTED: Bet with 'VOID' status is NOT displayed in 'Open Bets' tab
        """
        pass

    def test_008_repeat_steps_2_9_for_bet_slip_widget_for_tabletdesktop_open_bets_page_for_tabletdesktop___can_be_accessed_via_direct_link(self):
        """
        DESCRIPTION: Repeat steps 2-9 for:
        DESCRIPTION: * 'Bet Slip' widget (for Tablet/Desktop)
        DESCRIPTION: * Open Bets page (for Tablet/Desktop) - can be accessed via direct link
        EXPECTED: 
        """
        pass
