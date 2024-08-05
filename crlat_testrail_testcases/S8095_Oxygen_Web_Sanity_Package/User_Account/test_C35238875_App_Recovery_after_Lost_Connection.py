import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C35238875_App_Recovery_after_Lost_Connection(Common):
    """
    TR_ID: C35238875
    NAME: App Recovery after Lost Connection
    DESCRIPTION: This test case verifies that application is recovered after lost connection
    PRECONDITIONS: There are In-Play and Featured events available
    PRECONDITIONS: To trigger lost connection/reconnect:
    PRECONDITIONS: - turn internet off/on
    PRECONDITIONS: - lock/unlock the phone for >5 min
    """
    keep_browser_open = True

    def test_001_load_homepage(self):
        """
        DESCRIPTION: Load Homepage
        EXPECTED: 
        """
        pass

    def test_002_log_in(self):
        """
        DESCRIPTION: Log In
        EXPECTED: User is logged in
        """
        pass

    def test_003_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_004_verify_whether_user_session_is_reconnected_and_user_is_logged_in(self):
        """
        DESCRIPTION: Verify whether user session is reconnected and user is logged in
        EXPECTED: User is logged in;
        EXPECTED: Balance is displayed;
        EXPECTED: The following pages can be opened and are displayed correctly:
        EXPECTED: - Deposit pages
        EXPECTED: - Withdrawal pages
        EXPECTED: - Cash Out
        EXPECTED: - Open Bets
        EXPECTED: - Bet History
        """
        pass

    def test_005_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: 
        """
        pass

    def test_006_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_007_place_a_bet_via_quick_bet(self):
        """
        DESCRIPTION: Place a bet via Quick Bet
        EXPECTED: Bet can be placed successfully
        """
        pass

    def test_008_add_selection_to_betslip(self):
        """
        DESCRIPTION: Add selection to Betslip
        EXPECTED: 
        """
        pass

    def test_009_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_010_place_a_bet_from_betslip(self):
        """
        DESCRIPTION: Place a bet from Betslip
        EXPECTED: Bet can be placed successfully
        """
        pass

    def test_011_open_cash_out_page_with_available_bets_for_cash_out(self):
        """
        DESCRIPTION: Open Cash Out page with available bets for Cash Out
        EXPECTED: 
        """
        pass

    def test_012_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_013_perform_full_cash_out(self):
        """
        DESCRIPTION: Perform Full Cash Out
        EXPECTED: Cash Out is successful
        """
        pass

    def test_014_open_homepage_featured_tab(self):
        """
        DESCRIPTION: Open Homepage->Featured tab
        EXPECTED: 
        """
        pass

    def test_015_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_016_verify_featured_tab(self):
        """
        DESCRIPTION: Verify Featured tab
        EXPECTED: - Featured tab is displayed correctly;
        EXPECTED: - Featured modules are present and are up to date;
        EXPECTED: - Events are being updated
        """
        pass

    def test_017_open_in_play_page(self):
        """
        DESCRIPTION: Open In-Play page
        EXPECTED: 
        """
        pass

    def test_018_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_019_verify_in_play_page(self):
        """
        DESCRIPTION: Verify In-Play page
        EXPECTED: - In-Play page is displayed (Live Now, Upcoming, Sports filters);
        EXPECTED: - Events are present and are up to date;
        EXPECTED: - Events are being updated
        """
        pass

    def test_020_open_any_sports_page_eg_football(self):
        """
        DESCRIPTION: Open any <Sports> page (e.g. Football)
        EXPECTED: 
        """
        pass

    def test_021_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: 
        """
        pass

    def test_022_verify_sports_page(self):
        """
        DESCRIPTION: Verify <Sports> page
        EXPECTED: - <Sports> page is displayed
        EXPECTED: - Events are present and are up to date(no duplicates);
        EXPECTED: - Events are being updated
        EXPECTED: - All accordions can be expanded/collapsed
        EXPECTED: - Market selector works fine
        """
        pass
