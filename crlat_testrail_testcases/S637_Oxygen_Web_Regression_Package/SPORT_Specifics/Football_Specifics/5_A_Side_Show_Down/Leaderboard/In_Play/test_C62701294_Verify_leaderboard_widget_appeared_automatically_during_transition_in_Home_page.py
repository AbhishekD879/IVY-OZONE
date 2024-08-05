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
class Test_C62701294_Verify_leaderboard_widget_appeared_automatically_during_transition_in_Home_page(Common):
    """
    TR_ID: C62701294
    NAME: Verify leaderboard widget appeared automatically during transition in Home page
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

    def test_001_login_to_sportsbook_application_with_user_that_has_entered_into_any_pre_event_contest(self):
        """
        DESCRIPTION: Login to sportsbook application with user that has entered into any pre event contest
        EXPECTED: User should be logged in
        """
        pass

    def test_002_navigate_to_home_page(self):
        """
        DESCRIPTION: Navigate to home page
        EXPECTED: User should be navigated to home page
        """
        pass

    def test_003_wait_for_events_transition_from_pre_to_live(self):
        """
        DESCRIPTION: Wait for event's transition from pre to live
        EXPECTED: Event transition should be done
        """
        pass

    def test_004_observe_lb_widget_is_displayed_automatically_in_home_page(self):
        """
        DESCRIPTION: Observe LB widget is displayed automatically in home page
        EXPECTED: Leaderboard widget should be displayed automatically without any refresh
        """
        pass
