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
class Test_C62701301_Verify_LB_widget_data_is_in_sync_with_live_LB_data(Common):
    """
    TR_ID: C62701301
    NAME: Verify LB widget data is in sync with live LB data
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: 4: Event should start and User should enter the contest for the Leaderboard widget to be displayed
    PRECONDITIONS: Configurations for Leaderboard widget
    PRECONDITIONS: 1: Home Page
    PRECONDITIONS: 2: Football Page
    PRECONDITIONS: 3: My Bets
    PRECONDITIONS: CMS admin user should be able to enable/ disable the above toggles
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
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_login_to_sportsbook_application_with_user_that_has_entered_into_more_than_1_live_event_contests(self):
        """
        DESCRIPTION: Login to sportsbook application with user that has entered into more than 1 live event contests
        EXPECTED: User should be logged in
        """
        pass

    def test_002_navigate_to_fbhome_page(self):
        """
        DESCRIPTION: Navigate to fb/home page
        EXPECTED: User should be navigated to fb/home page
        """
        pass

    def test_003_verify_progress_bar_scores_timer_ranks_and_prizes_are_displaying_correctly_as_in_live_leaderboard(self):
        """
        DESCRIPTION: Verify progress bar, scores, timer, ranks and prizes are displaying correctly as in live leaderboard
        EXPECTED: Progress bar, scores, timer, ranks and prizes should be displayed correctly as in live leaderboard
        """
        pass
