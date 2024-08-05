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
class Test_C62701291_Verify_leaderboard_widget_appeared_in_home_page_on_login_with_user_that_has_entry_for_a_live_contest(Common):
    """
    TR_ID: C62701291
    NAME: Verify leaderboard widget appeared in home page on login with user that has entry for a live contest
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

    def test_001_launch_to_sportsbook_application_and_login_with_user_that_has_entered_into_any_live_contest(self):
        """
        DESCRIPTION: Launch to sportsbook application and login with user that has entered into any live contest
        EXPECTED: User should be logged in and should be in homepage
        """
        pass

    def test_002_observe_leaderboard_widget_is_displayed_in_home_page_automatically_as_soon_as_user_logged_in(self):
        """
        DESCRIPTION: Observe leaderboard widget is displayed in home page automatically as soon as user logged in
        EXPECTED: Leaderboard widget should be displayed automatically
        """
        pass
