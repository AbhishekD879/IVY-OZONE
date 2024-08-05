import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64377614_Verify_stats_are_updated_during_grace_period(Common):
    """
    TR_ID: C64377614
    NAME: Verify stats are updated during grace period
    DESCRIPTION: Verify stats are updated during grace period which is after ERT is sent and before header is received.
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: Create multiple contests for different events
    PRECONDITIONS: Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: 5) Wait for Event to start
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_login_to_sportsbook_with_user_that_satisfies_pre_conditions(self):
        """
        DESCRIPTION: Login to sportsbook with user that satisfies pre conditions
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_live_leaderboard(self):
        """
        DESCRIPTION: Navigate to live leaderboard
        EXPECTED: User should be navigated to LLB
        """
        pass

    def test_003_send_ertwhich_is_replay_incident___replay_stat_in_tst0_wait_until_event_is_finishedhlv0(self):
        """
        DESCRIPTION: Send ERT(which is replay incident _ replay stat in tst0)/ wait until event is finished(hlv0)
        EXPECTED: ERT should be received
        """
        pass

    def test_004_send_any_stat(self):
        """
        DESCRIPTION: Send any stat
        EXPECTED: Stat should be sent successfully
        """
        pass

    def test_005_observe_stat_is_updated_in_leaderboard(self):
        """
        DESCRIPTION: Observe stat is updated in leaderboard
        EXPECTED: Stat should be updated in LB
        """
        pass

    def test_006_at_9th_min_from_1st_ert_send_1_more_stat(self):
        """
        DESCRIPTION: At 9th min from 1st ERT, send 1 more stat
        EXPECTED: Stat should be updated in LB
        """
        pass

    def test_007_at_10th_min_send_stat_and_observe_in_fe(self):
        """
        DESCRIPTION: At 10th min, send stat and observe in FE
        EXPECTED: Stat should be updated and header should be received
        """
        pass

    def test_008_at_11th_min_send_1_more_stat_and_observe_in_fe(self):
        """
        DESCRIPTION: At 11th min send 1 more stat and observe in FE
        EXPECTED: Stat should be sent but it should not be updated in FE
        """
        pass
