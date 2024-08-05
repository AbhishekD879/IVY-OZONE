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
class Test_C61619048_Verify_display_of_order_of_Prizes_in_Leaderboard_Live_Event(Common):
    """
    TR_ID: C61619048
    NAME: Verify display of order of Prizes in  Leaderboard -Live Event
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

    def test_004_in_cms_configure_more_than_2_prizes_for_the_same_event_with_prize_text(self):
        """
        DESCRIPTION: In CMS, configure more than 2 prizes for the same event with Prize text.
        EXPECTED: * In Live Leader board, it should show in the below order.
        EXPECTED: *Cash-Voucher-FreeBet-Ticket*
        EXPECTED: * Only two prizes should be displayed in Live leader board.
        EXPECTED: * Prize text is not displayed in Live Leader Board for any prize only in Live Leader board.
        """
        pass

    def test_005_in_cms_configure_ticket_for_any_position_with_any_prize_value_signposting__prize_text(self):
        """
        DESCRIPTION: In CMS, configure ticket for any position with any Prize value, Signposting & Prize text.
        EXPECTED: * In Live Leader board, it should only show the SVG icon.
        EXPECTED: * Prize test, Prize value should not be displayed for Ticket only in Live Leader board.
        """
        pass
