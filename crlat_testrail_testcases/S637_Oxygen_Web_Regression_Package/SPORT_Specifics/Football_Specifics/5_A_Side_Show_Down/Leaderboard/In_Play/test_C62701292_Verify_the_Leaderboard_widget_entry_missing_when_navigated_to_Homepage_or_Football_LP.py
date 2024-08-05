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
class Test_C62701292_Verify_the_Leaderboard_widget_entry_missing_when_navigated_to_Homepage_or_Football_LP(Common):
    """
    TR_ID: C62701292
    NAME: Verify the Leaderboard widget entry missing when navigated to Homepage or Football LP
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

    def test_001_launch_to_sportsbook_application(self):
        """
        DESCRIPTION: Launch to sportsbook application
        EXPECTED: Sportbook should be launched
        """
        pass

    def test_002_navigate_to_football_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to football sports landing page
        EXPECTED: User should be navigated to FB page
        """
        pass

    def test_003_login_with_user_that_has_entered_into_any_live_contest(self):
        """
        DESCRIPTION: Login with user that has entered into any live contest
        EXPECTED: User should be loggedin with user thta has entered into any live contest
        """
        pass

    def test_004_observe_leaderboard_widget_is_displayed_in_fb_page_automatically_as_soon_as_user_logged_in(self):
        """
        DESCRIPTION: Observe leaderboard widget is displayed in FB page automatically as soon as user logged in
        EXPECTED: Leaderboard widget should be displayed automatically
        """
        pass

    def test_005_navigate_to_homepagefootball_lp_from_live_leaderboard_page(self):
        """
        DESCRIPTION: Navigate to Homepage/Football LP from Live leaderboard page
        EXPECTED: When navigated to Homepage or Football page from Live leaderboard data should be displayed with entry of best position and Progress should be updated dynamically.
        """
        pass
