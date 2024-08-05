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
class Test_C28080_Main_Navigation_functionality_on_Universal_Header_for_DesktopNot_valid_for_vanilla(Common):
    """
    TR_ID: C28080
    NAME: Main Navigation functionality on Universal Header for Desktop(Not valid for vanilla)
    DESCRIPTION: Please note: this test case is not valid for Vanilla.
    DESCRIPTION: This test case verifies Main Navigation functionality on Universal Header for Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    DESCRIPTION: Autotest: C2688242: https://ladbrokescoral.testrail.com/index.php?/cases/view/2688242
    PRECONDITIONS: * Main Navigation menu items should be configured in CMS ('Menus' > 'Header Menus') (refer to TC: https://ladbrokescoral.testrail.com/index.php?/cases/view/28124)
    PRECONDITIONS: * The following menu items should be created:
    PRECONDITIONS: 1) with '/' in 'Target uri'
    PRECONDITIONS: 2) with relative path in 'Target uri'
    PRECONDITIONS: 3) with absolute path in 'Target uri'
    PRECONDITIONS: 4) with 'In App' ticked
    PRECONDITIONS: 5) with 'In App' unticked
    PRECONDITIONS: * Oxygen app is loaded on desktop
    """
    keep_browser_open = True

    def test_001_verify_main_navigation_menu(self):
        """
        DESCRIPTION: Verify 'Main Navigation' menu
        EXPECTED: 'Main Navigation' menu consists of tabs that are CMS configurable
        """
        pass

    def test_002_verify_default_menu_item(self):
        """
        DESCRIPTION: Verify default menu item
        EXPECTED: * Menu item that has '/' set in 'Target uri' in CMS is default one
        EXPECTED: * Default menu item is selected when loading the app
        """
        pass

    def test_003_verify_order_of_main_navigation_menu_items(self):
        """
        DESCRIPTION: Verify order of 'Main Navigation' menu items
        EXPECTED: 'Main Navigation' menu items are ordered as in CMS
        """
        pass

    def test_004_hover_the_mouse_over_menu_items_in_main_navigation(self):
        """
        DESCRIPTION: Hover the mouse over menu items in 'Main Navigation'
        EXPECTED: Text color on tabs changes on mouse hover over
        """
        pass

    def test_005_click_on_any_tab_in_main_navigation_menu(self):
        """
        DESCRIPTION: Click on any tab in 'Main Navigation' menu
        EXPECTED: * All tabs are clickable
        EXPECTED: * Background color on tab is changed
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        """
        pass
