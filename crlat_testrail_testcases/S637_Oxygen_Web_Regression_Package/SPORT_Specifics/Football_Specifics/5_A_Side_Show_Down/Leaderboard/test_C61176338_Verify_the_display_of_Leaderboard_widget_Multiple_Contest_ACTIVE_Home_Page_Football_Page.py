import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C61176338_Verify_the_display_of_Leaderboard_widget_Multiple_Contest_ACTIVE_Home_Page_Football_Page(Common):
    """
    TR_ID: C61176338
    NAME: Verify the display of Leaderboard widget Multiple Contest ACTIVE- Home Page & Football Page
    DESCRIPTION: This test case verifies the display of Leaderboard Widget in Home page and Football landing page
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: 4: Event should start and User should enter the contest for the Leaderboard widget to be displayed
    PRECONDITIONS: **Configurations for Leaderboard widget**
    PRECONDITIONS: 1: Home Page
    PRECONDITIONS: 2: Football Page
    PRECONDITIONS: 3: My Bets
    PRECONDITIONS: CMS admin user should be able to enable/ disable the above toggles
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: **To Qualify for Showdown**
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_verify_the_display_of_leaderboard_widget_in_home_pagecontest_started_and_user_participated_in_that_contest(self):
        """
        DESCRIPTION: Verify the display of Leaderboard widget in **Home Page**
        DESCRIPTION: **Contest started and User Participated in that Contest**
        EXPECTED: * Leaderboard widget is displayed below the Highlights tab in Home Page
        EXPECTED: * ONLY in **Mobile** Leaderboard should be displayed when toggle is **ON** in CMS
        """
        pass

    def test_002_verify_the_display_of_leaderboard_widget_in_football_landing_pagecontest_started_and_user_participated_in_that_contest(self):
        """
        DESCRIPTION: Verify the display of Leaderboard widget in **Football Landing page**
        DESCRIPTION: **Contest started and User Participated in that Contest**
        EXPECTED: * Leaderboard widget is displayed below the Matches tab in Football Landing Page
        EXPECTED: * ONLY in **Mobile** Leaderboard should be displayed when toggle is **ON** in CMS
        """
        pass

    def test_003_verify_the_display_of_leaderboard_widget_as_carousal_when_multiple_showdowns_are_active_at_same_time(self):
        """
        DESCRIPTION: Verify the display of Leaderboard widget as Carousal when **Multiple Showdowns are ACTIVE at same time**
        EXPECTED: * Leaderboard widget should be displayed as Carousal
        EXPECTED: * Swipe Horizontal - other Showdown event widget should be displayed
        EXPECTED: * Updated Scores and positions should be displayed
        EXPECTED: **Showdown widget displayed is based on the priority defined in the CMS**
        """
        pass
