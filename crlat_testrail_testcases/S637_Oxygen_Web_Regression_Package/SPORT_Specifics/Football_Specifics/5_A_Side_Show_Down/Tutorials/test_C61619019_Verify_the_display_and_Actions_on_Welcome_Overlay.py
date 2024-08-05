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
class Test_C61619019_Verify_the_display_and_Actions_on_Welcome_Overlay(Common):
    """
    TR_ID: C61619019
    NAME: Verify the display and Actions on Welcome Overlay
    DESCRIPTION: This Test Case Verifies display and Actions on Welcome Overlay
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
    PRECONDITIONS: Item Label:Showdown Overlay
    PRECONDITIONS: Path: /five-a-side-showdown/welcome-overlay
    PRECONDITIONS: **Tutorial should be enabled in CMS**
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

    def test_001_login_ladbrokes(self):
        """
        DESCRIPTION: Login Ladbrokes
        EXPECTED: User should be able to login to Ladbrokes successfully
        """
        pass

    def test_002_navigate_first_time_to_showdown_lobby_page(self):
        """
        DESCRIPTION: Navigate first time to Showdown Lobby Page
        EXPECTED: User should be displayed with the Welcome Overlay
        EXPECTED: Welcome Overlay should be displayed as per design
        EXPECTED: Text and Video should be driven from CMS
        EXPECTED: ![](index.php?/attachments/get/151796659)
        """
        pass

    def test_003_verify_the_display_of_below_content_on_welcome_overlay_video_play_button_get_started(self):
        """
        DESCRIPTION: Verify the display of below content on Welcome Overlay
        DESCRIPTION: * Video Play Button
        DESCRIPTION: * Get Started
        EXPECTED: Video Play and Get Started Buttons should be displayed
        """
        pass

    def test_004_tap_on_video_play_button_and_verify_ga_tracking(self):
        """
        DESCRIPTION: Tap on Video Play Button and verify GA Tracking
        EXPECTED: Video should be played successfully and the action should be GA Tracked
        """
        pass

    def test_005_verify_the_interaction_of_video_controls(self):
        """
        DESCRIPTION: Verify the interaction of video controls
        EXPECTED: User should be able to interact with video controls
        """
        pass

    def test_006_tap_on_get_started_button_button_and_verify_ga_tracking(self):
        """
        DESCRIPTION: Tap on Get Started button Button and verify GA Tracking
        EXPECTED: Welcome Overlay should be closed and the action is GA Tracked
        """
        pass

    def test_007_clear_the_cache_and_navigate_to_pre_event_leaderboardrepeat_3_6(self):
        """
        DESCRIPTION: Clear the cache and navigate to Pre-Event Leaderboard
        DESCRIPTION: Repeat 3-6
        EXPECTED: User should be able to perform the actions successfully
        """
        pass

    def test_008_clear_the_cache_and_navigate_to_live_event_leaderboardrepeat_3_6(self):
        """
        DESCRIPTION: Clear the cache and navigate to Live-Event Leaderboard
        DESCRIPTION: Repeat 3-6
        EXPECTED: User should be able to perform the actions successfully
        """
        pass
