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
class Test_C62700894_Verify_the_font_styling_of_My_Entries_Leaderboard_Top_100_All_My_Entries_labels_in_Live_leaderboard(Common):
    """
    TR_ID: C62700894
    NAME: Verify the font styling of  My Entries , Leaderboard Top 100, All My Entries labels in Live leaderboard.
    DESCRIPTION: Verify the font styling of  My Entries , Leaderboard Top 100, All My Entries labels in Live leaderboard.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2)  user should not placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: Rules Entry Area
    PRECONDITIONS: Create  Rules Entry Area in CMS Static blocks
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_place_5_a_side_valid_bet(self):
        """
        DESCRIPTION: Place 5-a-side valid bet
        EXPECTED: User should able to entry to leaderboard contest
        """
        pass

    def test_003_validate_the_display_font_styling_of__my_entries__leaderboard_top_100_all_my_entries_labels_in_live_leaderboard(self):
        """
        DESCRIPTION: Validate the display font styling of  My Entries , Leaderboard Top 100, All My Entries labels in Live leaderboard.
        EXPECTED: font styling for the titles - My Entries , Leaderboard Top 100, All My Entries should display in "HelveticaNeue-Bold"
        """
        pass
