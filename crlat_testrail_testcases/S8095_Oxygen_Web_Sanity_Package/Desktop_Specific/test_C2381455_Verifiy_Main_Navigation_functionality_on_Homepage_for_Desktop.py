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
class Test_C2381455_Verifiy_Main_Navigation_functionality_on_Homepage_for_Desktop(Common):
    """
    TR_ID: C2381455
    NAME: Verifiy Main Navigation functionality on Homepage for Desktop
    DESCRIPTION: This test case verifies Main Navigation functionality on Homepage for Desktop.
    DESCRIPTION: Covered in AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=735048&group_order=asc
    PRECONDITIONS: 1. Open Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Items from 'Main Navigation', 'Sub Navigation' and 'Left Navigation' menus are CMS configurable.
    PRECONDITIONS: 1. 'Main Navigation' menu is configured by GVС
    PRECONDITIONS: 2. 'Sub Navigation'  menu  is configured in CMS: Menus -> Header SubMenu
    PRECONDITIONS: 3. 'Left Navigation'  menu  is configured in CMS: Menus -> Sport Categories
    """
    keep_browser_open = True

    def test_001_verify_universal_header_content_for_the_logged_out_user(self):
        """
        DESCRIPTION: Verify Universal Header content for the logged out user
        EXPECTED: Following elements are displayed:
        EXPECTED: * 'Coral'/'Ladbrokes' logo
        EXPECTED: * 'Main Navigation' menu configured by GVC
        EXPECTED: * 'Join' button
        EXPECTED: * 'Log in' button
        """
        pass

    def test_002_verify_universal_header_content_for_the_logged_in_user(self):
        """
        DESCRIPTION: Verify Universal Header content for the logged in user
        EXPECTED: The following items are displayed in the Universal header:
        EXPECTED: * 'Coral'/'Ladbrokes' logo
        EXPECTED: * 'Main Navigation' menu configured by GVC
        EXPECTED: * 'Balance' item with currency symbol and user's balance amount
        EXPECTED: * 'Deposit' Button
        EXPECTED: * 'My Account' item
        """
        pass

    def test_003_verify_items_displaying_on_main_navigation_menu(self):
        """
        DESCRIPTION: Verify items displaying on 'Main Navigation' menu
        EXPECTED: * 'Main Navigation' menu consists of tabs, that are configured by GVC
        EXPECTED: * SPORTS
        EXPECTED: * GAMING
        EXPECTED: * SLOTS
        EXPECTED: * LIVE CASINO
        EXPECTED: * CASINO
        EXPECTED: * BINGO
        EXPECTED: * POKER
        EXPECTED: * PROMOTIONS
        EXPECTED: * EXCHANGE
        EXPECTED: * THE GRID (or CONNECT for Coral)
        EXPECTED: * 'Sports' tab is selected by default
        """
        pass

    def test_004_click_on_some_item_from_main_navigation_menu(self):
        """
        DESCRIPTION: Click on some item from 'Main Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened
        EXPECTED: * 'Main Navigation' menu is still displayed
        """
        pass

    def test_005_verify_items_displaying_on_sub_navigation_menu(self):
        """
        DESCRIPTION: Verify items displaying on 'Sub Navigation' menu
        EXPECTED: * 'Sub Navigation' menu consists of tabs, that are CMS configurable:
        EXPECTED: * Home
        EXPECTED: * Promotions
        EXPECTED: * In-Play
        EXPECTED: * Football
        EXPECTED: * Horse Racing
        EXPECTED: * Tennis
        EXPECTED: * Build Your Bet
        EXPECTED: * Virtual Sports
        EXPECTED: * #Yourcall
        EXPECTED: * Greyhounds
        EXPECTED: * News & Blogs
        EXPECTED: * None tab is not selected by default
        """
        pass

    def test_006_click_on_some_item_from_sub_navigation_menu(self):
        """
        DESCRIPTION: Click on some item from 'Sub Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        EXPECTED: * 'Sub Navigation' menu is still displayed
        """
        pass

    def test_007_verify_the_left_navigation_menu_displaying(self):
        """
        DESCRIPTION: Verify the 'Left Navigation' menu displaying
        EXPECTED: * 'Left Navigation' menu is displayed on every page across the app
        EXPECTED: * 'A-Z Sports' inscription is displayed at the top of 'Left Navigation' menu
        EXPECTED: * 'Left Navigation' menu consists of CMS configurable items that are displayed vertically
        """
        pass

    def test_008_select_some_item_on_left_navigation_menu(self):
        """
        DESCRIPTION: Select some item on 'Left Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        EXPECTED: * 'Left Navigation' menu is still displayed
        EXPECTED: * All items within 'Left Navigation' menu are sorted in alphabetical order
        """
        pass
