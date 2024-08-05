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
class Test_C61619057_Verify_the_display_of_Tutorial_button_Lobby_Tutorial(Common):
    """
    TR_ID: C61619057
    NAME: Verify the display of Tutorial button_Lobby Tutorial
    DESCRIPTION: This test case verifies the display of Tutorial button Lobby Tutorial
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

    def test_001_launch_ladbrokes(self):
        """
        DESCRIPTION: Launch Ladbrokes
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_perform_login(self):
        """
        DESCRIPTION: Perform Login
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_003_navigate_to_5_a_side_lobby(self):
        """
        DESCRIPTION: Navigate to 5-A Side Lobby
        EXPECTED: * Tutorial button is displayed as per the design
        """
        pass

    def test_004_tap_on_tutorial_button(self):
        """
        DESCRIPTION: Tap on Tutorial button
        EXPECTED: * Tutorial is initiated
        EXPECTED: * Welcome to the Showdown Lobby Screen
        EXPECTED: * Text is driven from CMS
        EXPECTED: * Close button is available that shuts the experience
        EXPECTED: * 'Next' button takes customer to Step 2
        """
        pass

    def test_005_click_on_next(self):
        """
        DESCRIPTION: Click on Next
        EXPECTED: * Showdown card present in the Upcoming Showdowns list
        EXPECTED: * Display Prize screen as per design
        EXPECTED: * First Showdown card in the Upcoming Showdowns List (Today, Tomorrow etc) section is focused on
        EXPECTED: * Prize areas are highlighted as per the designs
        EXPECTED: * Text is driven from CMS
        EXPECTED: * Close button is available that shuts the experience
        EXPECTED: * Next' button takes customer to Step 3
        """
        pass

    def test_006_when_there_is_no_card(self):
        """
        DESCRIPTION: **When there is no Card**
        EXPECTED: IF no Showdown card is available in the Upcoming Showdowns List, then automatically end the Tutorial experience before displaying this screen.
        """
        pass

    def test_007_click_on_next(self):
        """
        DESCRIPTION: Click on NEXT
        EXPECTED: * Display Entry Stake screen as per design
        EXPECTED: * Entry Stake area is highlighted as per the design
        EXPECTED: * Text is driven from CMS
        EXPECTED: * Close button is available that shuts the experience
        EXPECTED: * 'Next' button takes customer to Step 4
        """
        pass

    def test_008_click_on_next(self):
        """
        DESCRIPTION: Click on NEXT
        EXPECTED: * Display the Finish screen as per designs
        EXPECTED: * The first Showdown card in the Upcoming Showdowns List (Today, Tomorrow etc) section is highlighted as per the designs
        EXPECTED: * Text is driven from CMS
        EXPECTED: * Close button is available that shuts the experience
        EXPECTED: * 'Finish' button shuts the experience
        """
        pass
