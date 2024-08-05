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
class Test_C60544580_Verify_Leaderboard_Updates(Common):
    """
    TR_ID: C60544580
    NAME: Verify Leaderboard Updates
    DESCRIPTION: This Test case verifies the Leaderboard Updates dynamically for a Live Event
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

    def test_006_verify_the_update_animations(self):
        """
        DESCRIPTION: Verify the Update animations
        EXPECTED: * Progress bar updates for all entries and User's Teams should be done when update is received in WS.
        EXPECTED: * Entry Positions on the Leaderboard and User's personal board should be done when update is received in WS.
        """
        pass
