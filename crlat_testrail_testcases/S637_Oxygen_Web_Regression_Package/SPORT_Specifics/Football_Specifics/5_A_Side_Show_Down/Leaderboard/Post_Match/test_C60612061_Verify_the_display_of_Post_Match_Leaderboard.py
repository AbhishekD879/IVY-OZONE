import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.5_a_side
@vtest
class Test_C60612061_Verify_the_display_of_Post_Match_Leaderboard(Common):
    """
    TR_ID: C60612061
    NAME: Verify the display of Post Match Leaderboard
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
        EXPECTED: ![](index.php?/attachments/get/137661548)
        EXPECTED: ![](index.php?/attachments/get/137661549)
        """
        pass

    def test_005_validate_the_display_of_header_area_on_scroll(self):
        """
        DESCRIPTION: Validate the display of Header Area on Scroll
        EXPECTED: Header area should be collapsed and remains sticky
        EXPECTED: **NOTE: Same behaviour as Live Leaderboard**
        """
        pass

    def test_006_validate_the_display_of_rules_button(self):
        """
        DESCRIPTION: Validate the display of Rules button
        EXPECTED: * Rules button should be displayed as per designs
        EXPECTED: * On tapping Rules button, Rules overlay should be opened
        EXPECTED: * Rules button should be GA tagged
        EXPECTED: *NOTE: Same behavior as Live Leaderboard*
        """
        pass

    def test_007_validate_the_display_of_leaderboard(self):
        """
        DESCRIPTION: Validate the display of Leaderboard
        EXPECTED: * Leaderboard should be displayed showing the leading entries in the contest along with the prizes
        EXPECTED: * Display limit rules are still followed
        EXPECTED: * Team summary should be displayed on tapping on each entry
        """
        pass

    def test_008_validate_the_display_of_my_entries_widget(self):
        """
        DESCRIPTION: Validate the display of My Entries Widget
        EXPECTED: * **My Entry** or **My Entries**  widget should be displayed
        EXPECTED: * ALL the customer's teams should be stacked in order of finishing position with prizes at right most side like in LB for each entry
        EXPECTED: * User should be able to Expand teams as per leaderboard
        EXPECTED: * Positions summary widget should be displayed
        EXPECTED: ![](index.php?/attachments/get/137661555)
        EXPECTED: ![](index.php?/attachments/get/137661557)
        """
        pass

    def test_009_validate_the_updates_received(self):
        """
        DESCRIPTION: Validate the updates received
        EXPECTED: * After 15 minutes of event completion no more live data updates are required from the update service
        """
        pass

    def test_010_validate_the_availability_of_post_match_leaderboard(self):
        """
        DESCRIPTION: Validate the availability of Post Match Leaderboard
        EXPECTED: * All the leaderboard data should be displayed for 7 days in last 7 days section and should be removed after 7 days
        """
        pass

    def test_011_verify_the_expand_and_collapse_of_entries_in_post_match_leaderboard(self):
        """
        DESCRIPTION: Verify the expand and collapse of entries in Post match leaderboard.
        EXPECTED: * Entry should be expanded displaying Team Progress and collapsed properly.
        """
        pass
