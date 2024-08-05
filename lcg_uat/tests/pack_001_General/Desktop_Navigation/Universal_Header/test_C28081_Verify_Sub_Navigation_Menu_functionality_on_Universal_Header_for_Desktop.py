import pytest
import tests
from time import sleep
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28081_Verify_Sub_Navigation_Menu_functionality_on_Universal_Header_for_Desktop(BaseSportTest):
    """
    TR_ID: C28081
    VOL_ID: C9698262
    NAME: Verify Sub Navigation Menu functionality on Universal Header for Desktop
    DESCRIPTION: This test case verifies Sub Navigation Menu functionality on Universal Header for Desktop.
    PRECONDITIONS: 1. To open CMS use the next links:
    PRECONDITIONS: DEV: https://invictus.coral.co.uk/keystone/header-menus
    PRECONDITIONS: TST2: https://bm-cms-tst2-coral.symphony-solutions.eu/keystone/header-menus
    PRECONDITIONS: STG2: https://bm-cms-stg2-coral.symphony-solutions.eu/keystone/header-menus
    PRECONDITIONS: |||:LINK TITLE|:TARGET URI
    PRECONDITIONS: || A-Z Menu |  az-sports
    PRECONDITIONS: || In-Play |  in-play
    PRECONDITIONS: || Football |  football
    PRECONDITIONS: || Horse Racing |  horseracing
    PRECONDITIONS: || #YourCall |  yourcall
    PRECONDITIONS: || Virtuals Sports |  virtual-sports
    PRECONDITIONS: || Tennis |  tennis
    PRECONDITIONS: || Live Stream |  live-stream
    PRECONDITIONS: || News & Blog | http://news.coral.co.uk/
    PRECONDITIONS: || Coral Radio | http://commentariesv4.mediaondemand.net/?c=coral
    PRECONDITIONS: || Statistics |  http://www.stats.betradar.com/s4/?clientid=192
    PRECONDITIONS: For TST2 urls will be like: http://www-tst2.coral.co.uk/casino/top-games
    PRECONDITIONS: For STG:  http://www-stg1.coral.co.uk/casino/top-games
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Sub Navigation Menu tabs from CMS
        """
        submenu_tabs_cms = self.cms_config.get_header_submenus()
        self.__class__.expected_tabs_dict = OrderedDict()
        for tab_name in submenu_tabs_cms:
            if tab_name.get('linkTitle') and not tab_name['disabled']:
                self.expected_tabs_dict[tab_name['linkTitle'].strip().upper()] = tab_name

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.navigate_to_page(name=tests.HOSTNAME)
        self.site.wait_content_state(state_name='HomePage')

    def test_002_check_sub_navigation_menu(self):
        """
        DESCRIPTION: Check 'Sub Navigation' menu
        EXPECTED: 'Sub Navigation' menu consists of tabs, that are CMS configurable:
        EXPECTED: * A-Z Menu
        EXPECTED: * In-Play
        EXPECTED: * Football
        EXPECTED: * Horse Racing
        EXPECTED: * #YourCall
        EXPECTED: * Virtual Sports
        EXPECTED: * Tennis
        EXPECTED: * Live Stream
        EXPECTED: * News Blog
        EXPECTED: * Coral Radio
        EXPECTED: * Statistics
        """
        self.__class__.actual_sport_tabs = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(self.actual_sport_tabs, msg='No one submenu tabs found')
        for item in self.actual_sport_tabs.keys():
            self.assertIn(item, list(self.expected_tabs_dict.keys()),
                          msg=f'Actual menu items order: \n["{item}"] '
                              f'\nExpected: \n["{list(self.expected_tabs_dict.keys())}"]')

    def test_003_verify_that_none_tab_is_not_selected_by_default(self):
        """
        DESCRIPTION: Verify that none tab is not selected by default
        EXPECTED: * Homepage is opened
        EXPECTED: * 'Home' tab is highlighted as selected
        """
        self.site.wait_content_state('Homepage')
        if 'HOME' in self.actual_sport_tabs.keys():
            tab = self.actual_sport_tabs['HOME']
            self.assertTrue(tab.is_selected(), msg='"HOME" tab is not selected by default')
            for tab_name, tab in list(self.actual_sport_tabs.items()):
                if tab_name != 'HOME':
                    self.assertFalse(tab.is_selected(expected_result=False),
                                     msg=f'"{tab_name}" tab is selected by default')
        else:
            for tab_name, tab in self.actual_sport_tabs.items():
                self.assertFalse(tab.is_selected(expected_result=False),
                                 msg=f'"{tab_name}" tab is selected by default')

    def test_004_hover_the_mouse_over_the_tabs_in_sub_navigation_menu(self):
        """
        DESCRIPTION: Hover the mouse over the tabs in 'Sub Navigation' menu
        EXPECTED: Text color on tabs is changed
        """
        # ToDo: after VOL-1875 is resolved
        # if 'HOME' in self.actual_sport_tabs.keys():
        #     values = list(self.actual_sport_tabs.values())[1:]
        # else:
        #     values = self.actual_sport_tabs.values()
        # for tab in values:
        #     before = tab.text_color_value
        #     tab.mouse_over()
        #     color_change = self.site.header.wait_for_tab_color_change(tab, before)
        #     self.assertFalse(color_change, msg=f'Text color on "{tab.get_attribute("title")}" tab is not changed')

    def test_005_select_some_tab_in_sub_navigation_menu(self):
        """
        DESCRIPTION: Select some tab in ' Sub Navigation' menu
        EXPECTED: * All tabs are clickable
        EXPECTED: * Selected tab is highlighted by red line
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        """
        except_list = ['CASINO', '#YOURCALL', 'CORAL RADIO', 'BUILD YOUR BET', 'NEWS & BLOGS', '1-2-FREE', 'THE GRID',
                       'RACING SUPER SERIES', 'FOOTBALL SUPER SERIES', 'NEWS', 'LADBROKES ROCKY', 'CORAL RACING CLUB','CRC','LADBROKES POWERLEAGUE','LADBROKES LIVE']
        for name, tab in list(self.actual_sport_tabs.items()):
            self.actual_sport_tabs = self.site.header.sport_menu.items_as_ordered_dict
            if name in except_list:
                continue
            sleep(1)
            if name != 'HOME':
                self.actual_sport_tabs[name].click()
                self.site.wait_content_state_changed(timeout=10)
            cms_tab = self.expected_tabs_dict[name]
            uri = cms_tab['targetUri']
            sleep(5)
            if not cms_tab['inApp']:
                self.assertTrue(uri in self.device.get_current_url(),
                                msg=f'Actual opened window URL: \n"{self.device.get_current_url()}", '
                                    f'\nexpected configured in CMS: \n"{uri}"')
            else:
                self.assertTrue(self.actual_sport_tabs[name].is_selected(timeout=3),
                                msg=f'Selected "{name}" tab is not highlighted by red line')
                self.assertTrue(uri in self.device.get_current_url(),
                                msg=f'Actual opened window URL: \n"{self.device.get_current_url()}", '
                                    f'\nexpected configured in CMS: \n"{uri}"')

    def test_006_verify_sub_navigation_menu_if_there_are_no_set_items(self):
        """
        DESCRIPTION: Verify 'Sub Navigation' menu if there are no set items
        EXPECTED: 'Sub Navigation' menu is not displayed anymore
        """
        # There is no possibility to verify this step
        pass
