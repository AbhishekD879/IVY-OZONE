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
class Test_C62745258_Verify_Live_leaderboard_page_while_scrolling(Common):
    """
    TR_ID: C62745258
    NAME: Verify Live leaderboard page while scrolling.
    DESCRIPTION: 
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

    def test_001_login_to_the_ladbrokes_application(self):
        """
        DESCRIPTION: Login to the ladbrokes application
        EXPECTED: User should be able to login
        """
        pass

    def test_002_navigate_to_5_a_side_lobby_and_place_a_bet_on_a_contest_which_is_going_to_live(self):
        """
        DESCRIPTION: Navigate to 5-a-side lobby and place a bet on a contest which is going to live
        EXPECTED: Customer should be able to place bet on the contest
        """
        pass

    def test_003_verify_if_the_customer_has_got_entry_confirmation_message_and_is_qualified_for_the_contest(self):
        """
        DESCRIPTION: verify if the customer has got entry confirmation message and is qualified for the contest
        EXPECTED: Customer should be qualified for the contest
        """
        pass

    def test_004_make_sure_the_contest_has_100plus_entries(self):
        """
        DESCRIPTION: Make sure the contest has 100+ entries
        EXPECTED: Contest should have 100+ entries
        """
        pass

    def test_005_verify_the_display_of_leaderboard_when_the_matchevent_is_in_play(self):
        """
        DESCRIPTION: Verify the display of Leaderboard when the Match/Event is In-Play
        EXPECTED: Leaderboard should be displayed showing the leading entries in the contest
        """
        pass

    def test_006_verify_the_display_of_entries_in_leaderboard(self):
        """
        DESCRIPTION: Verify the display of entries in Leaderboard
        EXPECTED: Below should be displayed for the entries,
        EXPECTED: Position and Image - Image pulled from CMS &gt; Image
        EXPECTED: Manager
        EXPECTED: Username
        EXPECTED: Odds
        EXPECTED: Prize and Signposting
        EXPECTED: Progress bar
        """
        pass

    def test_007_verify_whether_the_page_is_live_leaderboard_page_is_scrollable_with_no_issues(self):
        """
        DESCRIPTION: Verify whether the page is live leaderboard page is scrollable with no issues
        EXPECTED: Leaderboard page should be scrollable with no issues
        EXPECTED: - Page struck shouldn't happen
        EXPECTED: - White/black screens shouldn't be seen while scrolling
        """
        pass
