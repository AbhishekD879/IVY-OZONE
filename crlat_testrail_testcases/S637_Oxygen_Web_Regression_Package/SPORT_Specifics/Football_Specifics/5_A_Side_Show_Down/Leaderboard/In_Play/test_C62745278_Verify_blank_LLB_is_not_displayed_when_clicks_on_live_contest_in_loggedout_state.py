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
class Test_C62745278_Verify_blank_LLB_is_not_displayed_when_clicks_on_live_contest_in_loggedout_state(Common):
    """
    TR_ID: C62745278
    NAME: Verify blank LLB is not displayed when clicks on live contest in loggedout state
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create multiple contests for different events
    PRECONDITIONS: 2. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  5-A-Side bet by selecting any contest with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: Ladbrokes application should be launched
        """
        pass

    def test_002_without_login_navigate_to_lobby(self):
        """
        DESCRIPTION: Without login, navigate to lobby
        EXPECTED: User should be navigated to lobby without login
        """
        pass

    def test_003_click_on_contest_which_is_in_live(self):
        """
        DESCRIPTION: Click on contest which is in live.
        EXPECTED: User should click on live contest
        """
        pass

    def test_004_observe_user_navigates_to_live_leaderboard_page_with_all_valid_data_displayed_and_no_blank_page_is_seen(self):
        """
        DESCRIPTION: Observe user navigates to live leaderboard page with all valid data displayed and no blank page is seen
        EXPECTED: User should be navigated to LLB  with all data displayed and no blank page should be seen
        """
        pass
