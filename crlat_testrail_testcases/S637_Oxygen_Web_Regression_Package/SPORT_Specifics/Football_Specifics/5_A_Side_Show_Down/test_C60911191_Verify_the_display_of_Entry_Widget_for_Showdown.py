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
class Test_C60911191_Verify_the_display_of_Entry_Widget_for_Showdown(Common):
    """
    TR_ID: C60911191
    NAME: Verify the display of Entry Widget for Showdown
    DESCRIPTION: This test case verifies the display of Entry Widget for showdown
    DESCRIPTION: * Home Page
    DESCRIPTION: * Football landing page
    DESCRIPTION: * Event Details Page
    DESCRIPTION: **Not applicable for Desktop**
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Active Showdown Contest should be available
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
        EXPECTED: User should be able to access the application
        """
        pass

    def test_002_configure_in_cms_entry_widget___toggle_on_for_home_pagenavigate_to_home_page(self):
        """
        DESCRIPTION: Configure in CMS: Entry Widget - Toggle **ON** for **Home page**
        DESCRIPTION: Navigate to Home page
        EXPECTED: * User should be able to view the entry widget for showdown in Home page
        EXPECTED: * **Contest Description** - This is pulled from the 'Description' field configured in CMS > Contest Details(It should truncate if flows into Event Date)
        EXPECTED: * **Event Start** should be displayed.If event starts on that day, show countdown clock HH:MM format with clock counting down every minute.If event does not start on that day, show date/time as per the designs
        EXPECTED: * **Logo** should be displayed as configured in Image Manager
        EXPECTED: * **Teams Playing** should be displayed and the flag images are displayed as configured in CMS > Asset Manager(Text stacks if team name is too long)
        EXPECTED: * **Background** - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * **Button** should be displayed and the text should be as configured in CMS > Showdown Widget
        EXPECTED: ![](index.php?/attachments/get/137661563)
        """
        pass

    def test_003_configure_in_cms_entry_widget___toggle_on_for_football_landing_pagenavigate_to_football_landing_page_all_matches_tab(self):
        """
        DESCRIPTION: Configure in CMS: Entry Widget - Toggle **ON** for **Football Landing Page**
        DESCRIPTION: Navigate to Football Landing Page (All Matches Tab)
        EXPECTED: * User should be able to view the entry widget for showdown in Sports page as configured in CMS > Showdown Widget (Sport Category)
        EXPECTED: * Widget should be displayed underneath Matches tab
        EXPECTED: * **Contest Description** - This is pulled from the 'Description' field configured in CMS > Contest Details(It should truncate if flows into Event Date)
        EXPECTED: * **Event Start** should be displayed.If event starts on that day, show countdown clock HH:MM format with clock counting down every minute.If event does not start on that day, show date/time as per the designs
        EXPECTED: * **Logo** should be displayed as configured in Image Manager
        EXPECTED: * **Teams Playing** should be displayed and the flag images are displayed as configured in CMS > Asset Manager(Text stacks if team name is too long)
        EXPECTED: * **Background** - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * **Button** should be displayed and the text should be as configured in CMS > Showdown Widget
        EXPECTED: ![](index.php?/attachments/get/137661564)
        """
        pass

    def test_004_configure_in_cms_entry_widget___toggle_on_for_edpnavigate_to_edp_of_that_event_linked_to_contest(self):
        """
        DESCRIPTION: Configure in CMS: Entry Widget - Toggle **ON** for **EDP**
        DESCRIPTION: Navigate to EDP (of that event linked to Contest)
        EXPECTED: * User should be able to view the entry widget for showdown in Event details page as per the Event linked to Contest ID
        EXPECTED: * Widget should be displayed in All Markets tab as per the position configured in CMS
        EXPECTED: **Example:**
        EXPECTED: Position 0 = Above market 1
        EXPECTED: Position 1 = Below market 1
        EXPECTED: Position 2 = Below market 2
        EXPECTED: Position 3 = Below market 3
        EXPECTED: * **Contest Description** - This is pulled from the 'Description' field configured in CMS > Contest Details(It should truncate if flows into Event Date)
        EXPECTED: * **Event Start** should be displayed.If event starts on that day, show countdown clock HH:MM format with clock counting down every minute.If event does not start on that day, show date/time as per the designs
        EXPECTED: * **Logo** should be displayed as configured in Image Manager
        EXPECTED: * **Teams Playing** should be displayed and the flag images are displayed as configured in CMS > Asset Manager(Text stacks if team name is too long)
        EXPECTED: * **Background** - Green grassy background to the header (please view styles in terms of shadows and gradients)
        EXPECTED: * **Button** should be displayed and the text should be as configured in CMS > Showdown Widget
        EXPECTED: ![](index.php?/attachments/get/137661565)
        """
        pass

    def test_005_click_on_the_entry_widget_cta_buttonabove_steps_home_pagefootball_landing_pageedp(self):
        """
        DESCRIPTION: Click on the Entry Widget CTA button
        DESCRIPTION: (Above steps Home Page/Football Landing Page/EDP)
        EXPECTED: * User should be navigated to showdown Contest Page
        EXPECTED: * Button should be **GA tagged**
        """
        pass

    def test_006_disable_the_toggles_and_validate_that_entry_widget_is_not_displayed_home_page_football_landing_page_edp(self):
        """
        DESCRIPTION: Disable the toggles and Validate that entry widget is not displayed Home Page/ Football Landing page/ EDP
        EXPECTED: * Entry Widget should not be displayed
        """
        pass
