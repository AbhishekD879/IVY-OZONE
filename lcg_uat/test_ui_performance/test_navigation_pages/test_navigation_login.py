# coding=utf-8
import pytest

import voltron.environments.constants as vec
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_Login_navigation(BasePerformanceTest):
    """
    NAME: Performance test of 'Login' navigation
    """
    db_name = 'example3'
    measurement_name = 'Login navigation'

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
        self.site.login()
        self.device.driver.execute_script('return performance.mark("NEXTRACES_LOGIN_stop");')
        self.device.driver.execute_script('return performance.measure("NEXTRACES_LOGIN_navigation", '
                                          '"NEXTRACES_LOGIN_start", '
                                          '"NEXTRACES_LOGIN_stop");')

    def test_004_navigation_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My Bets' page
        EXPECTED: 'My Bets' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("LOGIN_MYBETS_start");')
        self.site.header.my_bets.click()
        self.device.driver.execute_script('return performance.mark("LOGIN_MYBETS_stop");')
        self.device.driver.execute_script('return performance.measure("LOGIN_MYBETS_navigation", '
                                          '"LOGIN_MYBETS_start", '
                                          '"LOGIN_MYBETS_stop");')

    def test_005_navigation_to_bet_history_page(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' page
        EXPECTED: 'Settled Bets' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("MYBETS_BETHISTORY_start");')
        self.site.cashout.tabs_menu.open_tab(vec.bet_history.SETTLED_BETS_TAB_NAME)
        self.device.driver.execute_script('return performance.mark("MYBETS_BETHISTORY_stop");')
        self.device.driver.execute_script('return performance.measure("MYBETS_BETHISTORY_navigation", '
                                          '"MYBETS_BETHISTORY_start", '
                                          '"MYBETS_BETHISTORY_stop");')

    def test_006_navigation_back_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My Bets' page
        EXPECTED: 'My Bets' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("BETHISTORY_MYBETS_start");')
        self.site.header.my_bets.click()
        self.device.driver.execute_script('return performance.mark("BETHISTORY_MYBETS_stop");')
        self.device.driver.execute_script('return performance.measure("BETHISTORY_MYBETS_navigation", '
                                          '"BETHISTORY_MYBETS_start", '
                                          '"BETHISTORY_MYBETS_stop");')

    def test_007_navigation_to_logout_page(self):
        """
        DESCRIPTION: Perform 'Logout'
        EXPECTED: 'Logout' is performed
        """
        self.device.driver.execute_script('return performance.mark("MYBETS_LOGOUT_start");')
        self.site.logout()
        self.device.driver.execute_script('return performance.mark("MYBETS_LOGOUT_stop");')
        self.device.driver.execute_script('return performance.measure("MYBETS_LOGOUT_navigation", '
                                          '"MYBETS_LOGOUT_start", '
                                          '"MYBETS_LOGOUT_stop");')
        self.post_to_influxdb()