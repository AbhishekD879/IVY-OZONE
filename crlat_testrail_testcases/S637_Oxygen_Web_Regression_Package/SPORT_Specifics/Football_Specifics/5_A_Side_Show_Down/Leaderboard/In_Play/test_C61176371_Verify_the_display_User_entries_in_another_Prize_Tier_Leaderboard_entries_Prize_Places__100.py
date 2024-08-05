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
class Test_C61176371_Verify_the_display_User_entries_in_another_Prize_Tier_Leaderboard_entries_Prize_Places__100(Common):
    """
    TR_ID: C61176371
    NAME: Verify the display User entries in another Prize Tier -Leaderboard entries (Prize Places > = 100)
    DESCRIPTION: This test case verifies the display of Leaderboard entries when Prize Places configured in CMS are greater than 500
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Prize Places configured in CMS should be greater than 500
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
        EXPECTED: The maximum entries displayed should be always displayed as 100.
        """
        pass

    def test_004_user_team_in_prize_places_in_100verify_the_display_of_users_teams(self):
        """
        DESCRIPTION: **User Team in Prize Places in 100**
        DESCRIPTION: Verify the display of User's Teams
        EXPECTED: * Teams are displayed in the relevant Position
        EXPECTED: * Teams should be highlighted as mentioned in the designs
        EXPECTED: ![](index.php?/attachments/get/161000444)
        """
        pass

    def test_005_user_team_in_prize_places_in_another_prize_tierverify_the_display_of_users_teams(self):
        """
        DESCRIPTION: **User Team in Prize Places in another prize Tier**
        DESCRIPTION: Verify the display of User's Teams
        EXPECTED: * Teams should be displayed before the bottom prize tier
        EXPECTED: * Teams should be highlighted as mentioned in the designs
        EXPECTED: * If the User Team is 120 position then Leaderboard entries should be displayed as
        EXPECTED: * Maximum of 100 entries should be displayed
        EXPECTED: * 100
        EXPECTED: * 120 (User Team)
        EXPECTED: ![](index.php?/attachments/get/161000443)
        """
        pass

    def test_006_user_team_not_in_prize_placesverify_the_display_of_users_teams(self):
        """
        DESCRIPTION: **User Team NOT in Prize Places**
        DESCRIPTION: Verify the display of User's Teams
        EXPECTED: * Teams are displayed at the bottom of Leaderboard
        EXPECTED: * A clear break beneath the Prize Place teams and the user's non-placing teams should be displayed as per the designs. Where 150 & 200 having different prizes configured.
        EXPECTED: * Teams should be highlighted as mentioned in the designs
        EXPECTED: * 1-100
        EXPECTED: * 150
        EXPECTED: * 200
        EXPECTED: * User Team
        EXPECTED: ![](index.php?/attachments/get/161000442)
        """
        pass

    def test_007_verify_leaderboard_scrolling(self):
        """
        DESCRIPTION: Verify Leaderboard Scrolling
        EXPECTED: * Experience should be smooth for the user and entries are already loaded on the page
        """
        pass
