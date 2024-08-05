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
class Test_C60911183_Verify_the_display_of_Ticket_Widget(Common):
    """
    TR_ID: C60911183
    NAME: Verify the display of Ticket Widget
    DESCRIPTION: This test case verifies the display of Ticket Widget in Showdown Header bar
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
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
    PRECONDITIONS: **Each ticket should be created in the Openbet with unique ID, these IDs will be set in the CMS.**
    """
    keep_browser_open = True

    def test_001_validate_the_display_of_ticket_widget_in_5_a_side_showdown_header_bar(self):
        """
        DESCRIPTION: Validate the display of Ticket Widget in 5-A-Side Showdown Header bar
        EXPECTED: * **Red Ticket Counter** - The number of Free Bet Tokens with ID(s) X that customer has in their account should be displayed (Token IDs and Ticket Name are pulled from 'Red Tickets' field in CMS)
        EXPECTED: * **Gold Ticket Counter** – The number of Free Bet Tokens with ID(s) X that customer has in their account should be displayed (Token IDs and Ticket Name are pulled from 'Gold Tickets' field in CMS
        EXPECTED: **NOTE** - If there is no Token ID entered in either of the Red Ticket or Gold Ticket fields in the CMS - then that Ticket counter will not be shown in the Ticket Widget
        """
        pass

    def test_002_click_on_the_dropdown(self):
        """
        DESCRIPTION: Click on the dropdown
        EXPECTED: * My Tickets should be displayed
        EXPECTED: * Text below the Ticket is displayed as configured in CMS
        EXPECTED: **Red Tickets** , **Gold Tickets** field in CMS
        EXPECTED: * Ticket summary should be displayed as per designs
        EXPECTED: * Ticket count should be displayed
        EXPECTED: * Ticket Summary should be displayed as configured in CMS > 5-A Side showdown > Ticket Management > Ticket Summary Text field
        EXPECTED: * **No Tickets**
        EXPECTED: * Summary should be displayed as configured in CMS > 5-A Side showdown > Ticket Management > No Tickets Summary field
        EXPECTED: ![](index.php?/attachments/get/137661561)
        EXPECTED: ![](index.php?/attachments/get/137661562)
        """
        pass

    def test_003_update_of_ticket_widget(self):
        """
        DESCRIPTION: Update of Ticket Widget
        EXPECTED: * **On Login** - When user logs in user related tickets should be updated and displayed
        EXPECTED: * On **Bet placement** with tickets- Tickets should be updated and displayed
        EXPECTED: * If the ticket is **expired** - Expired ticket should be removed and the same should be updated and displayed
        EXPECTED: * After **bet settlement** - if tickets are won the same should be updated and displayed
        """
        pass
