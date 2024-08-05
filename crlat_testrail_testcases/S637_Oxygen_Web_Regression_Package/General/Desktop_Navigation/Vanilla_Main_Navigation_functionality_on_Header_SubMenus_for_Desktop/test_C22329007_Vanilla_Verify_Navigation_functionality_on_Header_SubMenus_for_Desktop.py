import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C22329007_Vanilla_Verify_Navigation_functionality_on_Header_SubMenus_for_Desktop(Common):
    """
    TR_ID: C22329007
    NAME: [Vanilla]  Verify Navigation functionality on Header SubMenus for Desktop
    DESCRIPTION: This test case verifies Main Navigation functionality on Header SubMenus for Desktop
    PRECONDITIONS: Main Navigation menu items should be configured in CMS ('Menus' > 'Header SubMenus')
    PRECONDITIONS: The following menu items should be created:
    PRECONDITIONS: 1) with '/' in 'Target uri'
    PRECONDITIONS: 2) with relative path in 'Target uri'
    PRECONDITIONS: 3) with absolute path in 'Target uri'
    PRECONDITIONS: 4) with 'In App' ticked
    PRECONDITIONS: 5) with 'In App' unticked
    PRECONDITIONS: Vanilla app is loaded on desktop
    """
    keep_browser_open = True

    def test_001_verify_main_navigation_submenu(self):
        """
        DESCRIPTION: Verify 'Main Navigation' submenu
        EXPECTED: 'Main Navigation' submenu consists of tabs that are CMS configurable
        """
        pass

    def test_002_verify_default_menu_item(self):
        """
        DESCRIPTION: Verify default menu item
        EXPECTED: * Menu item that has '/' set in 'Target uri' in CMS is default one
        EXPECTED: * Default menu item is selected when loading the app
        """
        pass

    def test_003_verify_order_of_main_navigation_submenu_items(self):
        """
        DESCRIPTION: Verify order of 'Main Navigation' submenu items
        EXPECTED: 'Main Navigation' submenu items are ordered as in CMS
        """
        pass

    def test_004_hover_the_mouse_over_submenu_items_in_main_navigation(self):
        """
        DESCRIPTION: Hover the mouse over submenu items in 'Main Navigation'
        EXPECTED: Text color on tabs changes on mouse hover over
        """
        pass

    def test_005_click_on_any_tab_in_main_navigation_submenu(self):
        """
        DESCRIPTION: Click on any tab in 'Main Navigation' submenu
        EXPECTED: * All tabs are clickable
        EXPECTED: * Background color on tab is changed
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        """
        pass
