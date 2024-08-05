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
class Test_C61619054_Verify_the_display_of_Welcome_To_Showdown_Lobby_Lobby_Tutorial(Common):
    """
    TR_ID: C61619054
    NAME: Verify the display of Welcome To Showdown Lobby_Lobby Tutorial
    DESCRIPTION: This test case verifies the display of Showdown Lobby Tutorial Pages
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Lobby tutorial should be configured off in CMS.
    PRECONDITIONS: 4: User has placed 5-A Side bet successfully.
    PRECONDITIONS: 5: Navigate to 5-a-side lobby.
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

    def test_002_navigate_to_5_a_side_lobby(self):
        """
        DESCRIPTION: Navigate to 5-a-side lobby
        EXPECTED: Lobby should load with Animation and then lobby tutorial should be displayed with welcome overlay(Get Started)
        EXPECTED: ![](index.php?/attachments/get/161000233)
        """
        pass

    def test_003_click_on_get_started_button_and_verify_ga_tracking(self):
        """
        DESCRIPTION: Click on Get Started Button and verify GA tracking
        EXPECTED: **First Time User is navigated to this Page**
        EXPECTED: * Tutorial is initiated
        EXPECTED: * Welcome to the Showdown Lobby Screen
        EXPECTED: * Text is driven from CMS
        EXPECTED: * Close button is available that shuts the experience
        EXPECTED: * 'Next' button takes customer to another screen
        EXPECTED: ![](index.php?/attachments/get/151652632)
        """
        pass
