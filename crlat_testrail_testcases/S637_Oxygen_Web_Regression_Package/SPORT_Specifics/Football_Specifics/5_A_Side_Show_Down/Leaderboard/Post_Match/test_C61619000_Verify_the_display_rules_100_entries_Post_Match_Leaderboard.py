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
class Test_C61619000_Verify_the_display_rules_100_entries_Post_Match_Leaderboard(Common):
    """
    TR_ID: C61619000
    NAME: Verify the display rules < 100 entries _Post Match Leaderboard
    DESCRIPTION: This Test case verifies the display of Post Match Leaderboard
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: 4: Match should be completed
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

    def test_001_launch_ladbrokes(self):
        """
        DESCRIPTION: Launch Ladbrokes
        EXPECTED: User should be able to access Ladbrokes application
        """
        pass

    def test_002_navigate_to_post_match_leaderboard_page(self):
        """
        DESCRIPTION: Navigate to Post Match Leaderboard page
        EXPECTED: User should be navigated to Post Match Leaderboard page
        """
        pass

    def test_003_validate_the_display_of_post_event_leaderboard_content(self):
        """
        DESCRIPTION: Validate the display of Post Event Leaderboard Content
        EXPECTED: The following should be displayed when event is completed Live-Event Leaderboard changes to Post-Event Leaderboard.
        EXPECTED: * Header Area
        EXPECTED: * Rules
        EXPECTED: * My Entries Widget
        EXPECTED: * Leaderboard with Entries
        EXPECTED: Leaderboard is available to view and customers can interact with it as per normal, but live updates are no longer required and can be switched off 15 minutes after the event is complete
        """
        pass

    def test_004_validate_the_display_of_leaderboard(self):
        """
        DESCRIPTION: Validate the display of Leaderboard
        EXPECTED: * Leaderboard should be displayed showing the leading entries in the contest
        EXPECTED: * Display limit rules are still followed
        EXPECTED: * Team summary should be displayed on tapping on each entry
        """
        pass

    def test_005_verify_the_display_of_leaderboard_entries_when_size_is_less_than_100(self):
        """
        DESCRIPTION: Verify the display of Leaderboard entries when size is less than 100
        EXPECTED: * The maximum entries displayed should be the number of entries in contest
        EXPECTED: **Example:** If there are 50 entries in that contest ,leaderboard should display all 50 entries
        """
        pass
