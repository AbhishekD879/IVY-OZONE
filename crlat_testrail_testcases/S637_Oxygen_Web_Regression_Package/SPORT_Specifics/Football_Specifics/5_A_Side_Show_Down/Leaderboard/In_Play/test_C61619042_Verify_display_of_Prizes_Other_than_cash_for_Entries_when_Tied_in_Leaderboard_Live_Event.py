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
class Test_C61619042_Verify_display_of_Prizes_Other_than_cash_for_Entries_when_Tied_in_Leaderboard_Live_Event(Common):
    """
    TR_ID: C61619042
    NAME: Verify display of Prizes (Other than cash) for Entries when Tied in Leaderboard -Live Event
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

    def test_005_verify_the_display_of_positionverify_that_when_positions_are_tied_then_the_next_position_is_xplus_number_of_entries_tied_where_x_is_tied_postionposition_calculation____teams_are_ranked_based_on_total_progress_completed____any_teams_tied_on_progress_are_then_ranked_by_odds_highest_odds_the_better_position____any_teams_tied_on_progress_and_odds_are_tied_and_are_ordered_alphabetically_by_username(self):
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

    def test_006_display_of_prizeif_the_entry_with_one_type_of_prize_ticket_freebet_voucher_is_tied_with_another_entry_with_other_prizeticket_freebet_voucher(self):
        """
        DESCRIPTION: Display of Prize
        DESCRIPTION: **If the entry with one type of prize (Ticket, FreeBet, Voucher) is tied with another entry with other prize(Ticket, FreeBet, Voucher)**
        EXPECTED: * Prize Information should be displayed
        EXPECTED: * Signposting should be displayed
        EXPECTED: * If two or more entries are tied then the Prizes will be split based on the tie logic
        EXPECTED: **Tie Logic**
        EXPECTED: * Cash - Split over all positions
        EXPECTED: Example:
        EXPECTED: Position 5 = £10
        EXPECTED: Position 6 = £5
        EXPECTED: Position 7 = £2
        EXPECTED: and **3 teams are tied** for **5th**
        EXPECTED: then **£17 (£10 + £5 + £2 )**is split between the three teams
        EXPECTED: which is **17/3 = £5.6** and the next position paid a prize is 8th.
        EXPECTED: * Tickets, Vouchers and Free Bets - All tied positions get the same prize.
        EXPECTED: Example:
        EXPECTED: Position 10 = £15 Ticket and Position 11 = £10 Voucher and 2 teams are tied for 10th, then both are paid the same prize in full.
        EXPECTED: Position 10 = £15 Ticket
        EXPECTED: Position 11 = £15 Ticket
        """
        pass
