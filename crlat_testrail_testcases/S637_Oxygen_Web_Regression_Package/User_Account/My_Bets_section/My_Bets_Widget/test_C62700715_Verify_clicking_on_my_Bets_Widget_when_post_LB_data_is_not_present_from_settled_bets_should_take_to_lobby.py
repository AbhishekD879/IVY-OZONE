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
class Test_C62700715_Verify_clicking_on_my_Bets_Widget_when_post_LB_data_is_not_present_from_settled_bets_should_take_to_lobby(Common):
    """
    TR_ID: C62700715
    NAME: Verify clicking on my Bets Widget when post LB data is not present from settled bets should take to lobby
    DESCRIPTION: Verify clicking on my Bets Widget when post LB data is not present from settled bets should take to lobby
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
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
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_login_to_sportbook_with_user_that_has_normal_5_a_side_bets_placed(self):
        """
        DESCRIPTION: Login to sportbook with user that has normal 5-a-side bets placed
        EXPECTED: User should be logged into sportsbook
        """
        pass

    def test_002_navigate_to_my_bets___gtsettled_bets_after_7_days_of_contest_completion(self):
        """
        DESCRIPTION: Navigate to My bets --&gt;settled bets after 7 days of contest completion
        EXPECTED: User should navigate to My bets settled bets
        """
        pass

    def test_003_click_on_my_bets_widget_on_the_bet_that_has_entered_into_contest(self):
        """
        DESCRIPTION: Click on My bets widget on the bet that has entered into contest
        EXPECTED: User should clicked on my bets widget
        """
        pass

    def test_004_observe_user_is_navigated_to_lobby_when_post_leaderboard_is_not_available(self):
        """
        DESCRIPTION: Observe user is navigated to lobby, when post leaderboard is not available
        EXPECTED: User should be navigated to lobby when post leaderboard is not available
        EXPECTED: if available, navigate to event post llb
        """
        pass
