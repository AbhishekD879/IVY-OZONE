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
class Test_C62701300_Verify_contest_from_LB_widget_disappears_automatically_when_that_contest_has_transited_to_post_state_when_there_are_multiple_live_contests(Common):
    """
    TR_ID: C62701300
    NAME: Verify contest from LB widget disappears automatically when that contest has transited to post state when there are multiple live contests
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

    def test_003_wait_for_any_one_of_the_contest_to_get_transited_from_live_to_post(self):
        """
        DESCRIPTION: Wait for any one of the contest to get transited from live to post
        EXPECTED: One of the contest should be transited to post
        """
        pass

    def test_004_observe_that_contest_is_undisplayed_automatically_from_leaderboard_widget_and_remaining_live_contests_are_still_displayed(self):
        """
        DESCRIPTION: Observe that contest is undisplayed automatically from leaderboard widget and remaining live contests are still displayed
        EXPECTED: Contest which is in post state should be removed automatically from LB widget and remaining live contests should be displayed in LB widget
        """
        pass
