# coding=utf-8
import pytest

import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_My_Freebets_navigation(BasePerformanceTest):
    """
    NAME: Performance test of 'My Freebets' navigation
    """
    db_name = 'example3'
    measurement_name = 'My Freebets navigation'

    def test_001_load_home_page(self):
        """
        DESCRIPTION: Load 'Home' page
        EXPECTED: 'Home' page is loaded
        """
        self.navigate_to_url(self.test_hostname)

    def test_002_navigation_to_next_races_page(self):
        """
        DESCRIPTION: Navigate to 'Next Races' page
        EXPECTED: 'Next Races' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_NEXTRACES_start");')
        self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races))
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_NEXTRACES_stop");')
        self.device.driver.execute_script('return performance.measure("HOMEPAGE_NEXTRACES_navigation", '
                                          '"HOMEPAGE_NEXTRACES_start", '
                                          '"HOMEPAGE_NEXTRACES_stop");')

    def test_003_navigation_to_login_page(self):
        """
        DESCRIPTION: Perform 'Login'
        EXPECTED: 'Login' is performed
        """
        self.device.driver.execute_script('return performance.mark("NEXTRACES_LOGIN_start");')
        username = tests.settings.freebet_user
        self.site.login(username=username)
        self.device.driver.execute_script('return performance.mark("NEXTRACES_LOGIN_stop");')
        self.device.driver.execute_script('return performance.measure("NEXTRACES_LOGIN_navigation", '
                                          '"NEXTRACES_LOGIN_start", '
                                          '"NEXTRACES_LOGIN_stop");')

    def test_004_navigation_to_right_menu_button_tab(self):
        """
        DESCRIPTION: Navigate to 'Right menu button'
        EXPECTED: 'Right menu button' is navigated
        """
        self.device.driver.execute_script('return performance.mark("LOGIN_RIGHTMENU_start");')
        self.site.header.right_menu_button.click()
        self.device.driver.execute_script('return performance.mark("LOGIN_RIGHTMENU_stop");')
        self.device.driver.execute_script('return performance.measure("LOGIN_RIGHTMENU_navigation", '
                                          '"LOGIN_RIGHTMENU_start", '
                                          '"LOGIN_RIGHTMENU_stop");')

    def test_005_navigation_to_freebets_page(self):
        """
        DESCRIPTION: Navigate to 'Freebets' page
        EXPECTED: 'Freebets' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("RIGHTMENU_FREEBETS_start");')
        self.site.right_menu.click_item('MY FREEBETS & BONUSES')
        self.site.wait_content_state('Freebets')
        self.device.driver.execute_script('return performance.mark("RIGHTMENU_FREEBETS_stop");')
        self.device.driver.execute_script('return performance.measure("RIGHTMENU_FREEBETS_navigation", '
                                          '"RIGHTMENU_FREEBETS_start", '
                                          '"RIGHTMENU_FREEBETS_stop");')

    def test_006_navigation_to_logout_page(self):
        """
        DESCRIPTION: Perform 'Logout'
        EXPECTED: 'Logout' is performed
        """
        self.device.driver.execute_script('return performance.mark("FREEBETS_LOGOUT_start");')
        self.site.logout()
        self.device.driver.execute_script('return performance.mark("FREEBETS_LOGOUT_stop");')
        self.device.driver.execute_script('return performance.measure("FREEBETS_LOGOUT_navigation", '
                                          '"FREEBETS_LOGOUT_start", '
                                          '"FREEBETS_LOGOUT_stop");')
        self.post_to_influxdb()
