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
class Test_C60540544_Verify_the_display_of_Leaderboard_entries_Prize_Places_100(Common):
    """
    TR_ID: C60540544
    NAME: Verify the display of Leaderboard entries (Prize Places < 100)
    DESCRIPTION: This test case verifies the display of Leaderboard entries when Prize Places configured in CMS are less than 500
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Prize Places configured in CMS should be less than 500
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
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

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_5_a_side_showdown__contest__leaderboard(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown > Contest > Leaderboard
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_verify_the_display_of_leaderboard_entries_when_prize_places_configured_in_cms_are_less_than_100(self):
        """
        DESCRIPTION: Verify the display of Leaderboard entries when Prize places configured in CMS are less than 100
        EXPECTED: * The maximum entries displayed should be the number of Prize places
        EXPECTED: **Example:** If there are 70 Prize Places configured in CMS then the leaderboard should display All 70 entries
        """
        pass

    def test_004_verify_leaderboard_scrolling(self):
        """
        DESCRIPTION: Verify Leaderboard Scrolling
        EXPECTED: * Experience should be smooth for the user and entries are already loaded on the page
        """
        pass
