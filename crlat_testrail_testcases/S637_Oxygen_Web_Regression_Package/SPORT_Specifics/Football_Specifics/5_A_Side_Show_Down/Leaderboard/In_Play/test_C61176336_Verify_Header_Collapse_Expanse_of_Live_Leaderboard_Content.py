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
class Test_C61176336_Verify_Header_Collapse_Expanse_of_Live_Leaderboard_Content(Common):
    """
    TR_ID: C61176336
    NAME: Verify Header Collapse/Expanse of Live Leaderboard Content
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

    def test_003_verify_the_behavior_of_header_area_when_user_scrolls_down_the_page(self):
        """
        DESCRIPTION: Verify the behavior of Header area when user scrolls down the page
        EXPECTED: Header area should be collapsed and remains sticky
        EXPECTED: ![](index.php?/attachments/get/155995179)
        """
        pass

    def test_004_verify_the_behavior_of_header_area_when_user_scrolls_top_to_the_page(self):
        """
        DESCRIPTION: Verify the behavior of Header area when user scrolls top to the page
        EXPECTED: Header area should be expanded
        EXPECTED: ![](index.php?/attachments/get/130369482)
        """
        pass
