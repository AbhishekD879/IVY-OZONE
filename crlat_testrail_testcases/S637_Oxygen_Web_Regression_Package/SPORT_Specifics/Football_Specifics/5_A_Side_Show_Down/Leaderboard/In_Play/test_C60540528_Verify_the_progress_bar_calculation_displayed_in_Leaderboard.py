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
class Test_C60540528_Verify_the_progress_bar_calculation_displayed_in_Leaderboard(Common):
    """
    TR_ID: C60540528
    NAME: Verify the progress bar calculation displayed in Leaderboard
    DESCRIPTION: This Test case verifies the progress bar calculation displayed on Leaderboard for all the entries
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: 4: Event should be In-Play
    PRECONDITIONS: *Place bet with Clean sheet Market- To concede 0 goals*
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

    def test_003_verify_the_display_of_progress_bar_and_validate_the__calculation(self):
        """
        DESCRIPTION: Verify the display of progress bar and Validate the % calculation
        EXPECTED: * Progress bar should be displayed as per the Progress logic
        EXPECTED: * Progress % should be displayed
        EXPECTED: **Progress Logic**
        EXPECTED: * Each leg in the bet is worth 20%
        EXPECTED: * 5legs*20% = 100%
        EXPECTED: * Each leg has its own progress
        EXPECTED: **Example:**
        EXPECTED: * Kepa to Concede 1+ Goals (1/1)​ [20%]-- (1/1)*20 = 20
        EXPECTED: * Rudiger to Make 2+ Tackles (1/2)​ [10%] -- (1/2)*20 = 10
        EXPECTED: * Mount to Make 60+ Passes (15/60)​ [5%]-- (15/60)*20 = 5
        EXPECTED: * Jorginho to be Carded (Yes)​ [20%] --20
        EXPECTED: * Werner to Score 1+ Goal (0/1) [0%] -- 0
        EXPECTED: **Progress is 55%**
        """
        pass

    def test_004_verify_the_progress_displayed_for_clean_sheet_marketplace_bet_with_clean_sheet_market(self):
        """
        DESCRIPTION: Verify the progress displayed for Clean sheet Market
        DESCRIPTION: **Place bet with Clean sheet market**
        EXPECTED: * Progress for Clean sheet market should be displayed as **0%** until the match is completed
        """
        pass
