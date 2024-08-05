import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C64377611_Verify_header_is_received_after_10_minutes_from_ERT_and_stats_are_not_consumed_after_that(Common):
    """
    TR_ID: C64377611
    NAME: Verify header is received after 10 minutes from ERT and stats are not consumed after that
    DESCRIPTION: Verify header is received after 10 minutes from ERT and stats are not consumed after that
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

    def test_004_from_the_time_ert_sent_after_10_min_send_1_more_stat_in_tst0_observe_header_is_receivedverify_using_validate_header_flag_string_in_kibana(self):
        """
        DESCRIPTION: From the time ERT sent after 10 min, (send 1 more stat in tst0) observe header is received
        DESCRIPTION: Verify using "Validate header flag" string in kibana
        EXPECTED: Header should be true in kibana for that event
        """
        pass

    def test_005_send_1_more_stat_from_post_man(self):
        """
        DESCRIPTION: Send 1 more stat from post man
        EXPECTED: stat should be sent
        """
        pass

    def test_006_observe_stats_is_not_consumed(self):
        """
        DESCRIPTION: Observe stats is not consumed
        EXPECTED: Stats should not be consumed
        """
        pass
