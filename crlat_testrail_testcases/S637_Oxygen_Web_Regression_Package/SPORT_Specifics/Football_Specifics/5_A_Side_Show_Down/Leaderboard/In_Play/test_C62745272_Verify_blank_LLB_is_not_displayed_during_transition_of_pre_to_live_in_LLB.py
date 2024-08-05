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
class Test_C62745272_Verify_blank_LLB_is_not_displayed_during_transition_of_pre_to_live_in_LLB(Common):
    """
    TR_ID: C62745272
    NAME: Verify blank LLB is not displayed during transition of pre to live in LLB
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
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
    PRECONDITIONS: 4) Place  5-A-Side bet by selecting any contest with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_login_to_application_with_user_that_has_an_entry(self):
        """
        DESCRIPTION: Login to application with user that has an entry
        EXPECTED: User should be logged in
        """
        pass

    def test_002_navigate_to_lobby(self):
        """
        DESCRIPTION: Navigate to lobby
        EXPECTED: User should be navigated to lobby
        """
        pass

    def test_003_click_on_contest_which_is_in_pre_state(self):
        """
        DESCRIPTION: Click on contest which is in pre state
        EXPECTED: User should click on pre LB contest
        """
        pass

    def test_004_wait_for_transition_from_pre_to_live(self):
        """
        DESCRIPTION: Wait for transition from pre to live
        EXPECTED: User should be in pre LB
        """
        pass

    def test_005_after_transition_observe_live_leaderboard_is_loaded_successfully__and_no_blank_page_is_seen(self):
        """
        DESCRIPTION: After transition, observe live leaderboard is loaded successfully  and no blank page is seen
        EXPECTED: LLB with valid data should be displayed
        """
        pass
