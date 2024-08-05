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
class Test_C62700713_Verify_My_Bets_Widget_is_not_displayed_on_normal_5_a_side_bets_in_both_open_bets_and_settled_bets(Common):
    """
    TR_ID: C62700713
    NAME: Verify My Bets Widget is not displayed on normal 5-a-side bets in both open bets and settled bets
    DESCRIPTION: 
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
        EXPECTED: 2.User should navigate to My bets openbets/settled bets
        EXPECTED: 3. My bets widget should not be seen on 5-a-side bet which is not entered into any contest"
        """
        pass

    def test_002_navigate_to_my_bets_openbetssettled_bets(self):
        """
        DESCRIPTION: Navigate to My bets openbets/settled bets
        EXPECTED: User should navigate to My bets openbets/settled bets
        """
        pass

    def test_003_observe_my_bets_widget_is_not_present_on_5_a_side_bet_which_is_not_entered_into_any_contest(self):
        """
        DESCRIPTION: Observe My bets widget is not present on 5-a-side bet which is not entered into any contest
        EXPECTED: My bets widget should not be seen on 5-a-side bet which is not entered into any contest
        """
        pass
