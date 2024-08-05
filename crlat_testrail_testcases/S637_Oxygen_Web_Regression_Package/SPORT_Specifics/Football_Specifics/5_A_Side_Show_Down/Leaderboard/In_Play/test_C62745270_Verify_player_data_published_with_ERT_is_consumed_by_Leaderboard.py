import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C62745270_Verify_player_data_published_with_ERT_is_consumed_by_Leaderboard(Common):
    """
    TR_ID: C62745270
    NAME: Verify player data published with ERT is consumed by Leaderboard
    DESCRIPTION: This test case verifies the last player stat updates received with period code ERT should be consumed by Leaderboard.
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

    def test_001_navigate_to_live_leaderboard_and_check_for_player_stat_updates(self):
        """
        DESCRIPTION: Navigate to Live leaderboard and check for Player stat updates.
        EXPECTED: Stat updates are received and consumed by leaderboard.
        """
        pass

    def test_002_verify_the_last_update_received_after_end_of_the_match_it_should_have_period_code_as_ert_and_player_stat_data(self):
        """
        DESCRIPTION: Verify the last update received after end of the match, it should have period code as ERT and player stat data.
        EXPECTED: The player stats received along with Period code : ERT should be updated in entries and My entries in Leaderboard for that particular player.
        """
        pass
