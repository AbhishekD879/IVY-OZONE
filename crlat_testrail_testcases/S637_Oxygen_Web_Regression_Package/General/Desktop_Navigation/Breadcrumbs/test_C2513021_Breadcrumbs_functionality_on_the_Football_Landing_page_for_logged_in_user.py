import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2513021_Breadcrumbs_functionality_on_the_Football_Landing_page_for_logged_in_user(Common):
    """
    TR_ID: C2513021
    NAME: Breadcrumbs functionality on the Football Landing page for logged in user
    DESCRIPTION: This test case verifies breadcrumbs functionality on the Football Landing page for logged in user.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged in
    PRECONDITIONS: 3. Football Landing page is opened
    PRECONDITIONS: 4. 'Matches'->'Today' tab is opened by default
    PRECONDITIONS: **Note:**
    PRECONDITIONS: The chosen tab is recorded to Local Storage, in 'key' column see 'OX./football-tab-<username>' parameter and find <tab name> in 'value' column.
    PRECONDITIONS: CMS Configuration should be - Menus -> Header SubMenus Page -> Football -> Target Uri -> sport/football
    """
    keep_browser_open = True

    def test_001_verify_breadcrumbs_displaying_at_the_football_landing_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying at the Football Landing page
        EXPECTED: * Breadcrumbs are located below the 'Football' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Landing page:
        EXPECTED: 'Home' > 'Football' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_002_choose_outrights_tab_from_football_sub_tab_menu(self):
        """
        DESCRIPTION: Choose 'Outrights' tab from Football Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to selected tab (e.g. 'Outrights')
        """
        pass

    def test_003_navigate_to_outrights_event_page(self):
        """
        DESCRIPTION: Navigate to 'Outrights' event page
        EXPECTED: * Breadcrumbs are located below the 'Football' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Outright Event Details page: 'Home' > 'Football' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_004_click_on_football_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Football' hyperlink from the breadcrumbs
        EXPECTED: * Football Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Landing page:
        EXPECTED: 'Home' > 'Football' > 'Sub Tab Name' (Previously selected tab is opened (e.g. 'Outright') when navigating to Football Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_005_click_on_home_hyperlink__from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Home' hyperlink  from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        pass

    def test_006_navigate_to_football_landing_page_again_and_verify_which_tab_is_selected(self):
        """
        DESCRIPTION: Navigate to Football Landing page again and verify which tab is selected
        EXPECTED: * Breadcrumbs are located below the 'Football' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Football Landing page:
        EXPECTED: 'Home' > 'Football' > 'Sub Tab Name' (Remembered tab is selected in this case from step 4)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_007_repeat_steps_2_6_for_tabs_on_football_landing_page(self):
        """
        DESCRIPTION: Repeat steps 2-6 for tabs on Football Landing page
        EXPECTED: 
        """
        pass
