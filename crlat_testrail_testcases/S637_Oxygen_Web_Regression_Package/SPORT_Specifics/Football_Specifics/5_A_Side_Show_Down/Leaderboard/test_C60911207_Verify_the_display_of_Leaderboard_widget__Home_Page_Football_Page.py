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
class Test_C60911207_Verify_the_display_of_Leaderboard_widget__Home_Page_Football_Page(Common):
    """
    TR_ID: C60911207
    NAME: Verify the display of Leaderboard widget - Home Page & Football Page
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

    def test_003_verify_the_content_of_leaderboard_widget(self):
        """
        DESCRIPTION: Verify the content of Leaderboard widget
        EXPECTED: * 5-A-Side logo/background should be displayed as per the design
        EXPECTED: * Contest Summary(*Description* field in CMS) should be
        EXPECTED: displayed
        EXPECTED: * Team Names and flags should be displayed
        EXPECTED: * Score and Match Clock should be displayed
        EXPECTED: * Leaderboard Position should be displayed
        EXPECTED: * Username should be displayed (Same as in Leaderboard)
        EXPECTED: * Progress Bar should be displayed and updated
        EXPECTED: * Odds should be displayed
        EXPECTED: * Prize and Signposting should be displayed and updated
        """
        pass

    def test_004_click_on_the_leaderboard_widget_and_validate_the_navigation(self):
        """
        DESCRIPTION: Click on the Leaderboard Widget and Validate the navigation
        EXPECTED: * User should be navigated to the Live event Leaderboard page of that contest
        EXPECTED: * Click should be **GA tagged**
        """
        pass

    def test_005_verify_the_display_of_leaderboard_widget_when_user_has_multiple_teams(self):
        """
        DESCRIPTION: Verify the display of Leaderboard widget when User has **multiple Teams**
        EXPECTED: * Highest positioned team progress bar should be displayed in the widget
        EXPECTED: * Updated Scores and positions should be displayed
        """
        pass

    def test_006_verify_the_display_of_leaderboard_widget_as_carousal_when_multiple_showdowns_are_active_at_same_time(self):
        """
        DESCRIPTION: Verify the display of Leaderboard widget as Carousal when **Multiple Showdowns are ACTIVE at same time**
        EXPECTED: * Leaderboard widget should be displayed as Carousal
        EXPECTED: * Swipe Horizontal - other Showdown event widget should be displayed
        EXPECTED: * Updated Scores and positions should be displayed
        EXPECTED: **Showdown widget displayed is based on the priority defined in the CMS**
        """
        pass

    def test_007_verify_the_display_of_leaderboard_widget_on_event_completion(self):
        """
        DESCRIPTION: Verify the display of Leaderboard widget on **Event completion**
        EXPECTED: * Once the event is settled and is resulted flag is true Leaderboard widget for that Event should be removed
        """
        pass

    def test_008_disable_home_page_football_page_toggle_in_cms_and_validatecms__system_configuration__structure__fiveasideleaderboardwidget(self):
        """
        DESCRIPTION: Disable Home Page /Football Page toggle in CMS and Validate
        DESCRIPTION: CMS > System Configuration > Structure > FiveASideLeaderBoardWidget
        EXPECTED: **Home Page - Disable**
        EXPECTED: **Football Page - Enable**
        EXPECTED: * Leaderboard widget should **NOT** be displayed in Home page
        EXPECTED: * Leaderboard widget should be displayed in Football Page
        EXPECTED: **Home Page - Enable**
        EXPECTED: **Football Page - Disable**
        EXPECTED: * Leaderboard widget should be displayed in Home page
        EXPECTED: * Leaderboard widget should **NOT** be displayed in Football Page
        EXPECTED: **Home Page - Disable**
        EXPECTED: **Football Page - Disable**
        EXPECTED: * Leaderboard widget should **NOT** be displayed in Home page
        EXPECTED: * Leaderboard widget should **NOT** be displayed in Football Page
        """
        pass
