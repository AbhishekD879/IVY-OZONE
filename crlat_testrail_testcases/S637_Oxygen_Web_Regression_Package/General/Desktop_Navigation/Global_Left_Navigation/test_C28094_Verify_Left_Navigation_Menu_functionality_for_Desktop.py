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
class Test_C28094_Verify_Left_Navigation_Menu_functionality_for_Desktop(Common):
    """
    TR_ID: C28094
    NAME: Verify Left Navigation Menu functionality for Desktop
    DESCRIPTION: This test case verifies 'Left Navigation' menu functionality for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Left Navigation Menu Items are taken from CMS > sports-pages > sport-categories > sport e.g. Football > 'Show in AZ' should be checked
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_verify_the_left_navigation_menu_displaying(self):
        """
        DESCRIPTION: Verify the 'Left Navigation' menu displaying
        EXPECTED: * 'Left Navigation' menu is displayed on every page across the app
        EXPECTED: * 'A-Z Sports' inscription is displayed at the top of 'Left Navigation' menu
        EXPECTED: * 'Left Navigation' menu consists CMS configurable items that are displayed vertically
        """
        pass

    def test_003_hover_the_mouse_over_each_item_in_left_navigation_menu(self):
        """
        DESCRIPTION: Hover the mouse over each item in 'Left Navigation' menu
        EXPECTED: Hover state changes are activated on each item
        """
        pass

    def test_004_select_some_item_on_left_navigation_menu(self):
        """
        DESCRIPTION: Select some item on 'Left Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        EXPECTED: * 'Left Navigation' menu is still displayed
        """
        pass

    def test_005_verify_ordering_of_items_within_left_navigation_menu(self):
        """
        DESCRIPTION: Verify ordering of items within 'Left Navigation' menu
        EXPECTED: All items within 'Left Navigation' menu are sorted in alphabetical order
        """
        pass

    def test_006_navigate_across_the_application_and_verify_that_the_left_vertical_navigation_menu_is_displayed(self):
        """
        DESCRIPTION: Navigate across the application and verify that the left vertical navigation menu is displayed
        EXPECTED: 'Left Navigation' menu is still displayed after navigation to different pages across the app
        """
        pass
