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
class Test_C62701296_Verify_the_widget_is_added_in_homepage_when_other_contests_are_inplay_for_the_same_user(Common):
    """
    TR_ID: C62701296
    NAME: Verify the widget is added in homepage, when other contests are inplay for the same user
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

    def test_001_login_to_sportsbook_application_with_user_that_has_entered_into_two_or_more_different_events_contests(self):
        """
        DESCRIPTION: Login to sportsbook application with user that has entered into two or more different events contests
        EXPECTED: User should be logged in
        """
        pass

    def test_002_navigate_to_fbhomepage(self):
        """
        DESCRIPTION: Navigate to FB/homepage
        EXPECTED: User should be navigated to FB/Homepage
        """
        pass

    def test_003_after_1st_contest_is_live_widget_is_displayed_in_homefb_page(self):
        """
        DESCRIPTION: After 1st contest is live, widget is displayed in home/FB page
        EXPECTED: Widget should be displayed in home/fb page after 1st event transition
        """
        pass

    def test_004_wait_for_second_contest_pre_to_live_transition(self):
        """
        DESCRIPTION: Wait for second contest pre to live transition
        EXPECTED: Second contest transition should be done
        """
        pass

    def test_005_after_2nd_contest_transition_observe_that_contest_is_added_automatically_to_existing_widget(self):
        """
        DESCRIPTION: After 2nd contest transition, observe that contest is added automatically to existing widget
        EXPECTED: Second contest should be automatically added and displayed in leaderboard widget
        """
        pass
