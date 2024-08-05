import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C59115911_Verify_that_Banach_bets_are_correctly_displayed_in_Open_Bets_when_event_goes_live(Common):
    """
    TR_ID: C59115911
    NAME: Verify that Banach bets are correctly displayed in Open Bets when event goes live
    DESCRIPTION: This test case verifies that Banach bets are correctly displayed in Open Bets when event goes live
    PRECONDITIONS: To be tested after BMA-51747/BMA-53127 are done (~OX 104)
    PRECONDITIONS: 1. User is logged in.
    PRECONDITIONS: 2. User placed at least 3 bets on pre-play Banach event:
    PRECONDITIONS: - Bet-1 - one (or more) market/selection WITHOUT cashout option (usually some 'Player Bets' market don't have cashout available);
    PRECONDITIONS: - Bet-2 - one market/selection WITHOUT cashout and one WITH cashout (e.g. 'Player Bets' + 'Match Betting');
    PRECONDITIONS: - Bet-3 - one (or more) market/selection WITH cashout option available.
    PRECONDITIONS: 3. Event(s) (on which user placed bets) are Pre-Play (not started) on the moment of test case execution.
    """
    keep_browser_open = True

    def test_001_navigate_open_bets_page(self):
        """
        DESCRIPTION: Navigate Open Bets page
        EXPECTED: Open Bets page displayed
        """
        pass

    def test_002_check_3_bets_from_preconditions(self):
        """
        DESCRIPTION: Check 3 bets from preconditions
        EXPECTED: - All Bets displayed as active (not suspended)
        EXPECTED: - Bet1 - DOESN'T have cashout button
        EXPECTED: - Bet2 - DOESN'T have cashout button
        EXPECTED: - Bet3 - HAS cahout button present
        """
        pass

    def test_003_wait_until_events_goest_live_started_and_check_bets(self):
        """
        DESCRIPTION: Wait until event(s) goest Live (started) and check bets
        EXPECTED: - All Bets displayed as active (not suspended) (except the case when event becomes suspended)
        EXPECTED: - All Bets have 'Live' signposting icon
        EXPECTED: - Bet1 - DOESN'T have cashout button
        EXPECTED: - Bet2 - DOESN'T have cashout button
        EXPECTED: - Bet3 - HAS cashout button present
        """
        pass

    def test_004_monitor_bets_behaviour_for_updates_during_live_period(self):
        """
        DESCRIPTION: Monitor Bets behaviour for updates during Live period
        EXPECTED: Bets behave NOT same as regular (not Banach) bets, e.g.
        EXPECTED: - if event is suspended - text is greyed out and susp icon displayed
        EXPECTED: - if selection/market is suspended - bet is shown as active, without susp icon
        EXPECTED: - if cashout is not available (for Bet-3) - cashout button is not active and 'Cash Out Suspended' text displayed
        """
        pass
