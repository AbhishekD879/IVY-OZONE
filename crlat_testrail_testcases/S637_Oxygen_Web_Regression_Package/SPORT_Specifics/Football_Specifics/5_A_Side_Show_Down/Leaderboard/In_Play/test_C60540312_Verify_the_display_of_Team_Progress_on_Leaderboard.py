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
class Test_C60540312_Verify_the_display_of_Team_Progress_on_Leaderboard(Common):
    """
    TR_ID: C60540312
    NAME: Verify the display of Team Progress on Leaderboard
    DESCRIPTION: This test case verifies the Team progress that is displayed on Leaderboard when the event is Live
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
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

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should login successfully
        """
        pass

    def test_002_navigate_to_5_a_side_showdown__contest(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown > Contest
        EXPECTED: * User should be displayed Leaderboard
        EXPECTED: ![](index.php?/attachments/get/130369420)
        """
        pass

    def test_003_click_anywhere_on_the_entry(self):
        """
        DESCRIPTION: Click anywhere on the entry
        EXPECTED: * Entry should be expanded
        EXPECTED: * Entry Expansion should be **GA Tracked**
        EXPECTED: ![](index.php?/attachments/get/151652666)
        """
        pass

    def test_004_verify_the_team_progress_in_detailed_view(self):
        """
        DESCRIPTION: Verify the Team progress in detailed view
        EXPECTED: * Entry expands to show the detailed team progress with each leg of the bet displaying the following content:
        EXPECTED: * Selection Name
        EXPECTED: * Badge of Team
        EXPECTED: * Progress Bar
        EXPECTED: * Stat Count
        EXPECTED: * Win or Lost indicator (Tick or Cross)
        EXPECTED: * Ladbrokes 5-A-Side Watermark
        EXPECTED: * Team progress should follow all logic that is part of the My Bets Stat Tracking feature
        EXPECTED: * Team progress should be updated dynamically as per the update logic
        EXPECTED: ![](index.php?/attachments/get/151652668)
        """
        pass

    def test_005_verify_the_content_loading_on_expanding_the_entry(self):
        """
        DESCRIPTION: Verify the content loading on expanding the entry
        EXPECTED: * Animations should be displayed on the progress bars and ticks as per prototype (to follow from UX)
        """
        pass

    def test_006_click_on_the_expanded_entry_anywhere_not_including_the_team_progress_area(self):
        """
        DESCRIPTION: Click on the expanded entry anywhere *(not including the team progress area)*
        EXPECTED: * Entry should be collapsed to it's default state
        """
        pass

    def test_007_click_anywhere_on_any_entry_in_the_leaderboardafter_the_entry_expands_click_on_another_entry(self):
        """
        DESCRIPTION: Click anywhere on any entry in the Leaderboard
        DESCRIPTION: After the Entry Expands Click on another entry
        EXPECTED: * Entry should be expanded
        EXPECTED: **After the entry Expands**
        EXPECTED: * Already Expanded entry should be collapsed
        EXPECTED: * Entry Expands to show the Team progress
        EXPECTED: **Note:Two entries cannot be expanded at once**
        """
        pass
