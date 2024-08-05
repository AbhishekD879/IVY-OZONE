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
class Test_C62700710_Verify_clicking_on_my_Bets_Widget_from_openbets_takes_to_pre_live_leaderboard_of_that_bet(Common):
    """
    TR_ID: C62700710
    NAME: Verify clicking on my Bets Widget from openbets takes to pre/live leaderboard of that bet
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
        EXPECTED: User should be able login successfully
        """
        pass

    def test_002_navigate_to_my_bets__gtopenbets(self):
        """
        DESCRIPTION: Navigate to My bets--&gt;openbets
        EXPECTED: User should be able to navigate to openbets
        """
        pass

    def test_003_verify_clicking_on_my_bets_widget_navigates_to_pre_event_lb_if_event_has_not_yet_started_or_live_lb_if_event_gets_started(self):
        """
        DESCRIPTION: Verify clicking on My bets widget navigates to pre event LB if event has not yet started or live LB if event gets started.
        EXPECTED: User should be navigated to pre LB if event hasn't started or to live LB if event has started
        """
        pass
