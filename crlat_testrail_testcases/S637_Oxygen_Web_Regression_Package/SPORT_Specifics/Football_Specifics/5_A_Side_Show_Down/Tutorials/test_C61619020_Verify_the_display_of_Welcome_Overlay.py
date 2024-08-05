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
class Test_C61619020_Verify_the_display_of_Welcome_Overlay(Common):
    """
    TR_ID: C61619020
    NAME: Verify the display of Welcome Overlay
    DESCRIPTION: This Test Case Verifies the display Welcome Overlay for Showdown Lobby, Pre-Event Leaderboard and Live-Event Leaderboard pages when user launches first time
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

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_navigate_first_time_to_showdown_lobby_page(self):
        """
        DESCRIPTION: Navigate first time to Showdown Lobby page
        EXPECTED: User should be displayed with the Welcome Overlay
        EXPECTED: Welcome Overlay should be displayed as per design
        EXPECTED: ![](index.php?/attachments/get/161019211)
        """
        pass

    def test_003_navigate_first_time_to_below_pages_pre_event_leaderboard_live_event_leaderboard(self):
        """
        DESCRIPTION: Navigate first time to below pages
        DESCRIPTION: * Pre-Event Leaderboard
        DESCRIPTION: * Live-Event Leaderboard
        EXPECTED: User should not be displayed with the Welcome Overlay
        EXPECTED: **Example:**
        EXPECTED: Customer navigates to Showdown Lobby for first time - SHOW Welcome Overlay
        EXPECTED: Customer then navigates to Pre-Event or Live-Event Leaderboard for first time - DO NOT SHOW Welcome overlay, they have already seen it.
        """
        pass

    def test_004_clear_the_cache_and_navigate_first_time_to_pre_event_leaderboard(self):
        """
        DESCRIPTION: Clear the cache and Navigate first time to Pre-Event Leaderboard
        EXPECTED: User should be displayed with the Welcome Overlay
        EXPECTED: Welcome Overlay should be displayed as per design
        EXPECTED: ![](index.php?/attachments/get/161019213)
        """
        pass

    def test_005_navigate_first_time_to_below_pages_live_event_leaderboard_showdown_lobby(self):
        """
        DESCRIPTION: Navigate first time to below pages
        DESCRIPTION: * Live-Event Leaderboard
        DESCRIPTION: * Showdown Lobby
        EXPECTED: User should not be displayed with the Welcome Overlay
        """
        pass

    def test_006_clear_the_cache_and_navigate_first_time_to_live_event_leaderboard(self):
        """
        DESCRIPTION: Clear the cache and Navigate first time to Live-Event Leaderboard
        EXPECTED: User should be displayed with the Welcome Overlay
        EXPECTED: Welcome Overlay should be displayed as per design
        EXPECTED: ![](index.php?/attachments/get/161019214)
        """
        pass

    def test_007_navigate_first_time_to_below_pages_pre_event_leaderboard_showdown_lobby(self):
        """
        DESCRIPTION: Navigate first time to below pages
        DESCRIPTION: * Pre-Event Leaderboard
        DESCRIPTION: * Showdown Lobby
        EXPECTED: User should not be displayed with the Welcome Overlay
        """
        pass
