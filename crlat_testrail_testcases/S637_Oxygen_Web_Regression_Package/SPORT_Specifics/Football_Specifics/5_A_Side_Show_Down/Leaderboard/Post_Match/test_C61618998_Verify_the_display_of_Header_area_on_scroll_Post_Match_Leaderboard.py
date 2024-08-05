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
class Test_C61618998_Verify_the_display_of_Header_area_on_scroll_Post_Match_Leaderboard(Common):
    """
    TR_ID: C61618998
    NAME: Verify the display of  Header area on scroll-Post Match Leaderboard
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

    def test_004_validate_the_display_of_header_area(self):
        """
        DESCRIPTION: Validate the display of Header Area
        EXPECTED: * **Contest Description** - This is pulled from the 'Description' field (It should truncate if flows into Event Date)
        EXPECTED: * **Logo** - This is uploaded in the Image Manager
        EXPECTED: * **Background** - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * **Teams Playing** - The two teams playing and their associated images from the asset manager. (Text stacks if team name is too long)
        EXPECTED: * **Final Score** - This is the final score in the match.
        EXPECTED: *NOTE: If match goes to Penalties then Scoreline should reflect the score at the end of extra time.*
        EXPECTED: * **Full Time** - Clear signposting of 'Full Time' indicating that the event is over
        EXPECTED: ![](index.php?/attachments/get/161000056)
        """
        pass

    def test_005_validate_the_display_of_header_area_on_scroll(self):
        """
        DESCRIPTION: Validate the display of Header Area on Scroll
        EXPECTED: Header area should be collapsed and remains sticky
        EXPECTED: ![](index.php?/attachments/get/161000058)
        EXPECTED: **NOTE: Same behaviour as Live Leaderboard**
        """
        pass
