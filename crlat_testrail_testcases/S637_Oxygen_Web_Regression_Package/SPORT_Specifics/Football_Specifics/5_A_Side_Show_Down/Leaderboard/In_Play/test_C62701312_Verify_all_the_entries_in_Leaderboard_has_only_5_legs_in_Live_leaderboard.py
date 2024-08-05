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
class Test_C62701312_Verify_all_the_entries_in_Leaderboard_has_only_5_legs_in_Live_leaderboard(Common):
    """
    TR_ID: C62701312
    NAME: Verify all the entries in Leaderboard has only 5 legs in Live leaderboard.
    DESCRIPTION: This test case verifies the duplication of legs data for all entries in Live leaderboard.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: To Qualify for Showdown
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

    def test_002_navigate_to_5_a_side_showdown_gt_contest_gt_leaderboard(self):
        """
        DESCRIPTION: Navigate to 5-A Side showdown &gt; Contest &gt; Leaderboard
        EXPECTED: User should be navigated to Leaderboard page
        """
        pass

    def test_003_verify_the_progress_bar_updates(self):
        """
        DESCRIPTION: Verify the Progress bar updates
        EXPECTED: * No Page refresh should be needed
        EXPECTED: * Data should be updated automatically for every 30 seconds
        EXPECTED: * User Team progress bar and % should be automatically updated
        """
        pass

    def test_004_verify_the_progress_bar_updated_for_all_entries_and_user_teams(self):
        """
        DESCRIPTION: Verify the progress bar updated for all entries and User Teams
        EXPECTED: * No Page refresh should be needed
        EXPECTED: * Data should be updated automatically for every 30 seconds
        EXPECTED: * User Team progress bar and % should be automatically updated
        EXPECTED: * All entries on Leaderboard progress bar and % should be automatically updated
        """
        pass

    def test_005_verify_the_entry_positions_update(self):
        """
        DESCRIPTION: Verify the Entry Positions Update
        EXPECTED: * No Page refresh should be needed
        EXPECTED: * Data should be updated automatically for every 30 seconds
        EXPECTED: * User Team Entry Positions should be automatically updated within the personal Leaderboard and also on the Leaderboard
        EXPECTED: * All entries Positions on Leaderboard should be automatically updated
        """
        pass

    def test_006_verify_the_legs_for_all_entries_in_live_leaderboard(self):
        """
        DESCRIPTION: Verify the legs for all entries in Live leaderboard.
        EXPECTED: There should be only 5 legs for every entry in leaderboard.
        """
        pass
