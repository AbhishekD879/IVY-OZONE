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
class Test_C62700708_Verify_my_Bets_Widget_is_displayed_on_the_bets_that_are_entered_into_leaderboard_in_open_bets(Common):
    """
    TR_ID: C62700708
    NAME: Verify my Bets Widget is displayed on the bets that are entered into leaderboard in open bets
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

    def test_001_login_to_ladbrokes_sports_application(self):
        """
        DESCRIPTION: Login to ladbrokes sports application
        EXPECTED: User should be able to launch ladbrokes application successfully
        """
        pass

    def test_002_navigate_to_my_bets__gtopen_bets(self):
        """
        DESCRIPTION: Navigate to My bets--&gt;Open bets
        EXPECTED: Should be navigated to My bets--&gt;openbets
        """
        pass

    def test_003_verify_display_of_my_bets_widget_on_bet_that_entered_into_leaderboard(self):
        """
        DESCRIPTION: Verify display of My bets widget on bet that entered into Leaderboard
        EXPECTED: My bets widget should be displayed on bet that entered into Leaderboard in openbets
        """
        pass
