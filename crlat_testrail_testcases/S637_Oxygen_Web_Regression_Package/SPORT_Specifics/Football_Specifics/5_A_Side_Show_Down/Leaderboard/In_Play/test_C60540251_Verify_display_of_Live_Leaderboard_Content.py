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
class Test_C60540251_Verify_display_of_Live_Leaderboard_Content(Common):
    """
    TR_ID: C60540251
    NAME: Verify display of Live Leaderboard Content
    DESCRIPTION: This test case verifies the display of Leaderboard Content when the event is In-Play
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User has placed 5-A Side bet successfully
    PRECONDITIONS: **How to Configure Menu Item**
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Item Label: FAQs
    PRECONDITIONS: Path: /five-a-side-showdown/faq
    PRECONDITIONS: Item Label: Terms & Conditions
    PRECONDITIONS: Path: /five-a-side-showdown/terms-and-conditions
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

    def test_001_navigate_to_leaderboard_when_the_event_is_in_play(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is In-Play
        EXPECTED: User should be navigated to Leaderboard when the event is Inplay
        EXPECTED: ![](index.php?/attachments/get/130369480)
        """
        pass

    def test_002_verify_the_content_in_leaderboard_when_the_event_in_play(self):
        """
        DESCRIPTION: Verify the content in Leaderboard when the event In-Play
        EXPECTED: * User should be displayed with the below details:
        EXPECTED: * Header Area
        EXPECTED: * Rules Button
        EXPECTED: * My Entries Widget
        EXPECTED: * Leaderboard with Entries
        """
        pass

    def test_003_verify_the_position_of_header_area_in_leaderboard_when_the_event_in_play(self):
        """
        DESCRIPTION: Verify the position of Header area in Leaderboard when the event In-Play
        EXPECTED: * Header area should be displayed at top of the page with the below contents
        EXPECTED: * Contest Description - This is pulled from the 'Description' field from CMS
        EXPECTED: * Logo - This is uploaded in the Image Manager
        EXPECTED: * Background - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * Teams Playing - The two teams playing and their associated images from the asset manager. (Text stacks if team name is too long)
        EXPECTED: * Match Clock - This is the time in the match - dynamically ticks up
        EXPECTED: * Live Score - This is the score in the match - dynamically changes with every goal
        EXPECTED: * Match Clock and Live scores are updated along with the Game stats as per Opta Scoreboard
        """
        pass

    def test_004__verify_the_description_of_header_area__configured_in_cms__contest_details_page__description__enter_long_text_in_the_description_field_and_click_on_save(self):
        """
        DESCRIPTION: * Verify the description of Header area
        DESCRIPTION: *  [Configured in CMS > Contest Details page > 'Description']
        DESCRIPTION: *  Enter long text in the Description field and click on save
        EXPECTED: Contest Description should be truncated and it should not flow into Event Date
        """
        pass

    def test_005_verify_the_behavior_of_header_area_when_user_scrolls_down_the_page(self):
        """
        DESCRIPTION: Verify the behavior of Header area when user scrolls down the page
        EXPECTED: Header area should be collapsed and remains sticky
        EXPECTED: ![](index.php?/attachments/get/130369481)
        """
        pass

    def test_006_verify_the_behavior_of_header_area_when_user_scrolls_top_to_the_page(self):
        """
        DESCRIPTION: Verify the behavior of Header area when user scrolls top to the page
        EXPECTED: Header area should be expanded
        EXPECTED: ![](index.php?/attachments/get/130369482)
        """
        pass

    def test_007__verify_rules_button_click_on_rules_button(self):
        """
        DESCRIPTION: * Verify Rules Button
        DESCRIPTION: * Click on Rules Button
        EXPECTED: * User should able to view Rules Button
        EXPECTED: * Rules overlay should be displayed (BMA-58834)
        """
        pass

    def test_008_verify_ga_tracking_for_rules_button(self):
        """
        DESCRIPTION: Verify GA tracking for Rules Button
        EXPECTED: Rules Button should be GA tracked
        """
        pass
