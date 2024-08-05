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
class Test_C61619043_Verify_display_of_Entries_with_100_progress_bar_in_Leaderboard_Live_Event(Common):
    """
    TR_ID: C61619043
    NAME: Verify display of Entries with 100% progress bar in Leaderboard -Live Event
    DESCRIPTION: This test case verifies the display of Leaderboard when the Event is In-Play
    DESCRIPTION: 1: Position
    DESCRIPTION: 2: Entry Information
    DESCRIPTION: 3: Progress Bar
    DESCRIPTION: 4: Username
    DESCRIPTION: 5: Odds
    DESCRIPTION: 6: Prize and Signposting
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

    def test_003_verify_the_display_of_leaderboard_when_the_matchevent_is_in_play(self):
        """
        DESCRIPTION: Verify the display of Leaderboard when the Match/Event is In-Play
        EXPECTED: * Leaderboard should be displayed showing the leading entries in the contest
        EXPECTED: * Header text should be **Leaderboard Top [X]'**
        EXPECTED: *where X = 100*
        EXPECTED: ![](index.php?/attachments/get/130369422)
        """
        pass

    def test_004_verify_the_display_of_entries_in_leaderboard(self):
        """
        DESCRIPTION: Verify the display of entries in Leaderboard
        EXPECTED: Below should be displayed for the entries,
        EXPECTED: * Position and Image - Image pulled from CMS > Image
        EXPECTED: Manager
        EXPECTED: * Username
        EXPECTED: * Odds
        EXPECTED: * Prize and Signposting
        EXPECTED: * Progress bar
        EXPECTED: ![](index.php?/attachments/get/130369423)
        """
        pass

    def test_005_verify_the_username_displayed(self):
        """
        DESCRIPTION: Verify the Username displayed
        EXPECTED: * Username of the user who the entry belongs to should be displayed
        EXPECTED: * Username should be truncated and displayed with last three characters replaced by ***
        EXPECTED: If the user name has 5 - 8 characters should be as follows.
        EXPECTED: 5. 12345 ==> 12***
        EXPECTED: 6. 123456 ==> 123***
        EXPECTED: 7. 1234567 ==> 1234***
        EXPECTED: 8. 12345678 ==> 12345***
        EXPECTED: 9. 123456789 ==> 12345***
        """
        pass

    def test_006_verify_the_display_of_oddsuser_account__settings__betting_settingsindexphpattachmentsget130369425(self):
        """
        DESCRIPTION: Verify the display of Odds
        DESCRIPTION: *User Account > Settings > Betting Settings*
        DESCRIPTION: ![](index.php?/attachments/get/130369425)
        EXPECTED: **Fractional**
        EXPECTED: If the User global setting is Fractional then odds will be displayed in Fractional format
        EXPECTED: **Decimal**
        EXPECTED: If the User global setting is Decimal then odds will be displayed in Decimal format
        EXPECTED: Odds displayed on the entry should be same as the odds while placing bet
        """
        pass

    def test_007_verify_the_display_of_positionverify_that_when_positions_are_tied_then_the_next_position_is_xplus_number_of_entries_tied_where_x_is_tied_postionposition_calculation____teams_are_ranked_based_on_total_progress_completed____any_teams_tied_on_progress_are_then_ranked_by_odds_highest_odds_the_better_position____any_teams_tied_on_progress_and_odds_are_tied_and_are_ordered_alphabetically_by_username(self):
        """
        DESCRIPTION: Verify the display of Position
        DESCRIPTION: Verify that when positions are tied then the next position is (X+ number of entries tied) where X is tied postion
        DESCRIPTION: **Position Calculation**
        DESCRIPTION: ---> Teams are ranked based on total progress completed.
        DESCRIPTION: ---> Any teams tied on progress are then ranked by odds (Highest Odds the better position)
        DESCRIPTION: ---> Any teams tied on progress and odds are tied and are ordered alphabetically by username
        EXPECTED: * Current Position of the entry should be displayed based on the **Position Calculation**
        EXPECTED: * Position should be dynamically updated as per Update rules
        EXPECTED: **Tied Position**
        EXPECTED: * Tie should be displayed as *'X='*
        EXPECTED: where *X* is the entry highest position
        """
        pass

    def test_008_verify_display_of_progress_bar(self):
        """
        DESCRIPTION: Verify Display of Progress bar
        EXPECTED: * User should be able to view the progress bar and % indicating the progress of the bet as per the Progress Logic
        EXPECTED: * Progress bar should be updated dynamically as per the update rules
        EXPECTED: * When a Progress bar is 100% then entire progress bar should be filled blue and a green tick should be seen next to it.
        EXPECTED: ![](index.php?/attachments/get/150789350)
        """
        pass