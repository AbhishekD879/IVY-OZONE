import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62745269_Verify_for_stale_data_at_the_bottom_of_live_leaderboard(Common):
    """
    TR_ID: C62745269
    NAME: Verify for stale data at the bottom of live leaderboard.
    DESCRIPTION: This test case verifies the Stale data at the bottom of the Leaderboard when updates started to receive in Leaderboard.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_navigate_to_live_leaderboard_after_transition(self):
        """
        DESCRIPTION: Navigate to Live leaderboard after transition.
        EXPECTED: Leaderboard has dummy update with no Player stats updated.
        """
        pass

    def test_002_verify_the_stale_data_at_the_bottom_of_the_leaderboard_once_player_stats_are_updated(self):
        """
        DESCRIPTION: Verify the stale data at the bottom of the leaderboard once Player stats are updated.
        EXPECTED: There should be any stale data or duplicate positions at the bottom of Leaderboard.
        """
        pass
