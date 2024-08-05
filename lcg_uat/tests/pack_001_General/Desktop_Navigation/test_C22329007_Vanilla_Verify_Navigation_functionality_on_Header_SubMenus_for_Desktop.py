import pytest
import tests
from collections import OrderedDict
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.reg157_fix
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.desktop
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
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Header SubMenus tabs from CMS
        """
        self.__class__.submenu_tabs_cms = self.cms_config.get_header_submenus()
        self.__class__.expected_tabs_dict = OrderedDict()
        for tab_name in self.submenu_tabs_cms:
            if tab_name.get('linkTitle') and not tab_name['disabled']:
                self.expected_tabs_dict[tab_name['linkTitle'].strip().upper()] = tab_name

    def test_001_verify_main_navigation_submenu(self):
        """
        DESCRIPTION: Verify 'Main Navigation' submenu
        EXPECTED: 'Main Navigation' submenu consists of tabs that are CMS configurable
        """
        self.site.wait_content_state(state_name='HomePage')
        self.__class__.actual_sport_tabs = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(self.actual_sport_tabs, msg='No one submenu tabs found')
        self.__class__.expected_sub_header = list(self.expected_tabs_dict.keys())
        if self.brand == 'ladbrokes':
            self.expected_sub_header.remove('FANZONE')
            self.assertListEqual(list(self.actual_sport_tabs.keys()), self.expected_sub_header,
                             msg=f'Actual menu items order: \n["{list(self.actual_sport_tabs.keys())}"] '
                                 f'\nExpected: \n["{self.expected_sub_header}"]')
        else:
            self.assertListEqual(list(self.actual_sport_tabs.keys()), self.expected_sub_header,
                                 msg=f'Actual menu items order: \n["{list(self.actual_sport_tabs.keys())}"] '
                                     f'\nExpected: \n["{self.expected_sub_header}"]')

    def test_002_verify_default_menu_item(self):
        """
        DESCRIPTION: Verify default menu item
        EXPECTED: * Menu item that has '/' set in 'Target uri' in CMS is default one
        EXPECTED: * Default menu item is selected when loading the app
        """
        default_tab_name = None
        for tab_name in self.submenu_tabs_cms:
            if tab_name['targetUri'] == '/?automationtest=true':
                default_tab_name = tab_name.get('linkTitle').upper()

        for tab_name, tab in list(self.actual_sport_tabs.items()):
            if tab_name == default_tab_name:
                self.assertTrue(tab.is_selected(), msg='Tab that has "/" set in "Target uri" is not selected by default')
            else:
                self.assertFalse(tab.is_selected(expected_result=False), msg=f'"{tab_name}" tab is selected by default')

    def test_003_verify_order_of_main_navigation_submenu_items(self):
        """
        DESCRIPTION: Verify order of 'Main Navigation' submenu items
        EXPECTED: 'Main Navigation' submenu items are ordered as in CMS
        """
        order_status = []
        ui_tab_names = list(self.actual_sport_tabs.keys())
        cms_tab_names = self.expected_sub_header
        if len(ui_tab_names) == len(cms_tab_names):
            order_status = [i for i, j in zip(ui_tab_names, cms_tab_names) if i == j]
        self.assertEqual(order_status, ui_tab_names, msg='Submenu header item ordering is not same in UI and CMS')

    def test_004_hover_the_mouse_over_submenu_items_in_main_navigation(self):
        """
        DESCRIPTION: Hover the mouse over submenu items in 'Main Navigation'
        EXPECTED: Text color on tabs changes on mouse hover over
        """
        if 'HOME' in self.actual_sport_tabs.keys():
            values = list(self.actual_sport_tabs.values())[1:]
        else:
            values = self.actual_sport_tabs.values()
        if self.brand == 'bma':
            for tab in values:
                before = tab.text_color_value
                tab.mouse_over()
                color_change = self.site.header.wait_for_tab_color_change(tab, before)
                self.assertFalse(color_change, msg=f'Text color on "{tab.get_attribute("title")}" tab is not changed')
        else:
            for tab in values:
                text_opacity_before = tab.opacity_value
                tab.mouse_over()
                text_opacity_after = tab.opacity_value
                self.assertNotEqual(text_opacity_before, text_opacity_after,
                                    msg=f'Text color on "{tab.get_attribute("title")}" tab is not changed')

    def test_005_click_on_any_tab_in_main_navigation_submenu(self):
        """
        DESCRIPTION: Click on any tab in 'Main Navigation' submenu
        EXPECTED: * All tabs are clickable
        EXPECTED: * Background color on tab is changed
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        """
        except_list = ['HOME', 'FOOTBALL SUPER SERIES', 'CASINO', '#YOURCALL', 'CORAL RADIO', 'BUILD YOUR BET', 'NEWS & BLOGS', '1-2-FREE', 'THE GRID',
                       'RACING SUPER SERIES', 'CORRECT 4', '5-A-SIDE','LADBROKES POWERLEAGUE', 'CRC', 'CORAL RACING CLUB', 'LOBBY', 'LADBROKES LIVE']
        for name, tab in self.actual_sport_tabs.items():
            tab = self.actual_sport_tabs.get(name)
            if name in except_list:
                continue
            sleep(2)
            if name != 'HOME':
                tab.click()
            cms_tab = self.expected_tabs_dict[name]
            uri = cms_tab['targetUri']
            if not cms_tab['inApp']:
                self.site.wait_content_state_changed()
                sleep(3)
                self.__class__.actual_sport_tabs = self.site.header.sport_menu.items_as_ordered_dict
                tab = self.actual_sport_tabs.get(name)
            sleep(3)
            self.assertTrue(tab.is_selected(timeout=3),
                            msg=f'Selected "{name}" tab is not highlighted by red line')
            self.assertTrue(uri in self.device.get_current_url(),
                            msg=f'Actual opened window URL: \n"{self.device.get_current_url()}", '
                                f'\nexpected configured in CMS: \n"{uri}"')
