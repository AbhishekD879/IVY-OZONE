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
class Test_C62700714_Verify_GA_tracking_of_my_bets_widget_CTA(Common):
    """
    TR_ID: C62700714
    NAME: Verify GA tracking of my bets widget CTA
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
        """
        pass

    def test_002_navigate_to_my_bets_openbets_and_settled_bets(self):
        """
        DESCRIPTION: Navigate to My bets openbets and settled bets
        EXPECTED: User should navigate to My bets openbets/settled bets
        """
        pass

    def test_003_verify_ga_tracking_for_my_bets_widget(self):
        """
        DESCRIPTION: Verify GA tracking for my bets widget
        EXPECTED: My bets widget CTA should be GA tracked in both Openbets and settledbets
        """
        pass
