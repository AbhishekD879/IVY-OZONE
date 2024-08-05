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
class Test_C62745267_Verify_my_entries_updates_in_websocket_calls_in_Liveserve_MS(Common):
    """
    TR_ID: C62745267
    NAME: Verify my entries updates in websocket calls in Liveserve MS
    DESCRIPTION: This test case verifies the updates in liveserve microservice for My entries
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

    def test_001_navigate_to_live_leaderboard_and_login_with_an_user_having_teamteams_entered_into_the_contestgo_to_network___liveserve_call___messages(self):
        """
        DESCRIPTION: Navigate to Live leaderboard and login with an user having team/teams entered into the contest.
        DESCRIPTION: Go to Network - Liveserve call - Messages
        EXPECTED: Call with user name with every Stat update is recorded in Liveserve.
        EXPECTED: Ideally there will be call with every update for leaderboard.
        EXPECTED: There should not ne any redundant updates for My entry.
        """
        pass
