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
class Test_C62701290_Verify_if_the_post_leaderboard_is_navigating_to_post_leaderboard_page_in_logged_in_state(Common):
    """
    TR_ID: C62701290
    NAME: Verify if the post leaderboard is navigating to post leaderboard page in logged in state
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
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_launch_the_application_in_logged_out_state(self):
        """
        DESCRIPTION: Launch the application in logged out state
        EXPECTED: User should be able to launch the application in logged out state
        """
        pass

    def test_002_navigate_to_post_leaderboard_contest_and_check_if_the_post_leaderboard_data_is_displayed_after_settlement(self):
        """
        DESCRIPTION: Navigate to post leaderboard contest and check if the post leaderboard data is displayed after settlement
        EXPECTED: Post leaderboard data should be displayed till the data is present in backend
        """
        pass
