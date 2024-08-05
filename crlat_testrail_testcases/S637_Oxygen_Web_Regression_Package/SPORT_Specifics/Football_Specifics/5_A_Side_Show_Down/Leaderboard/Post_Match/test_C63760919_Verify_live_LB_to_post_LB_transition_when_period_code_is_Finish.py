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
class Test_C63760919_Verify_live_LB_to_post_LB_transition_when_period_code_is_Finish(Common):
    """
    TR_ID: C63760919
    NAME: Verify live LB to post LB transition when period code is 'Finish'
    DESCRIPTION: Verify live LB to post LB transition when period code is 'Finish'
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
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

    def test_001_login_to_sportsbook_with_user_that_satisfies_pre_conditions(self):
        """
        DESCRIPTION: Login to Sportsbook with user that satisfies pre conditions
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_live_leaderboard(self):
        """
        DESCRIPTION: Navigate to live leaderboard
        EXPECTED: User should be navigated to live leaderboard
        """
        pass

    def test_003_inspect_page_and_in_web_socket_call_observe_period_code(self):
        """
        DESCRIPTION: Inspect page and in web socket call, Observe period code
        EXPECTED: Period code should be seen
        """
        pass

    def test_004_as_soon_as_period_code_status_is_finish_live_leaderboard_page_is_navigated_automatically_to_post_leaderboard(self):
        """
        DESCRIPTION: As soon as period code status is 'Finish', live leaderboard page is navigated automatically to post leaderboard
        EXPECTED: Post leaderboard should be displayed correctly as soon as period code is finish
        """
        pass

    def test_005_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Post LB should be displayed without any issues
        """
        pass

    def test_006_navigate_to_lobby_and_open_post_lb(self):
        """
        DESCRIPTION: Navigate to lobby and open post LB
        EXPECTED: Post LB should be displayed correctly
        """
        pass
