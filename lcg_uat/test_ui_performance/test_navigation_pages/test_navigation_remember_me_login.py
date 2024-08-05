# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_Remember_me_Login_navigation(BasePerformanceTest):
    """
    NAME: Performance test of 'Remember me Login' navigation
    """
    db_name = 'example3'
    measurement_name = 'Remember me Login navigation'

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

    def test_003_navigation_to_remember_me_login_page(self):
        """
        DESCRIPTION: Perform 'Login' with remember me option
        EXPECTED: 'Login' is performed
        """
        self.device.driver.execute_script('return performance.mark("NEXTRACES_REMEMBERMELOGIN_start");')
        self.site.login(remember_me=True)
        self.device.driver.execute_script('return performance.mark("NEXTRACES_REMEMBERMELOGIN_stop");')
        self.device.driver.execute_script('return performance.measure("NEXTRACES_REMEMBERMELOGIN_navigation", '
                                          '"NEXTRACES_REMEMBERMELOGIN_start", '
                                          '"NEXTRACES_REMEMBERMELOGIN_stop");')

    def test_004_navigation_to_home_page(self):
        """
        DESCRIPTION: Navigate to 'Home' page
        EXPECTED: 'Home' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("REMEMBERMELOGIN_HOMEPAGE_start");')
        self.site.header.brand_logo.click()
        self.site.wait_content_state('Homepage')
        self.device.driver.execute_script('return performance.mark("REMEMBERMELOGIN_HOMEPAGE_stop");')
        self.device.driver.execute_script('return performance.measure("REMEMBERMELOGIN_HOMEPAGE_navigation", '
                                          '"REMEMBERMELOGIN_HOMEPAGE_start", '
                                          '"REMEMBERMELOGIN_HOMEPAGE_stop");')

    def test_005_navigation_to_logout_page(self):
        """
        DESCRIPTION: Perform 'Logout'
        EXPECTED: 'Logout' is performed
        """
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_LOGOUT_start");')
        self.site.logout()
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_LOGOUT_stop");')
        self.device.driver.execute_script('return performance.measure("HOMEPAGE_LOGOUT_navigation", '
                                          '"HOMEPAGE_LOGOUT_start", '
                                          '"HOMEPAGE_LOGOUT_stop");')
        self.post_to_influxdb()
