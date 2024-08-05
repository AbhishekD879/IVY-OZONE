# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_All_Sports_navigation(BasePerformanceTest):
    """
    NAME: Performance test of 'All Sports' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'All Sports navigation'

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

    def test_003_navigation_to_football_page(self):
        """
        DESCRIPTION: Navigate to 'Football' page
        EXPECTED: 'Football' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("NEXTRACES_FOOTBALL_start");')
        self.site.home.menu_carousel.click_item('FOOTBALL')
        self.device.driver.execute_script('return performance.mark("NEXTRACES_FOOTBALL_stop");')
        self.device.driver.execute_script('return performance.measure("NEXTRACES_FOOTBALL_navigation", '
                                          '"NEXTRACES_FOOTBALL_start", '
                                          '"NEXTRACES_FOOTBALL_stop");')

    def test_004_navigation_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' page
        EXPECTED: 'Horse Racing' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("FOOTBALL_HORSERACING_start");')
        self.site.header.brand_logo.click()
        self.site.wait_content_state('Homepage')
        self.site.home.menu_carousel.click_item('HORSE RACING')
        self.device.driver.execute_script('return performance.mark("FOOTBALL_HORSERACING_stop");')
        self.device.driver.execute_script('return performance.measure("FOOTBALL_HORSERACING_navigation", '
                                          '"FOOTBALL_HORSERACING_start", '
                                          '"FOOTBALL_HORSERACING_stop");')

    def test_005_navigation_to_tennis_page(self):
        """
        DESCRIPTION: Navigate to 'Tennis' page
        EXPECTED: 'Tennis' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("HORSERACING_TENNIS_start");')
        self.site.header.brand_logo.click()
        self.site.wait_content_state('Homepage')
        self.site.home.menu_carousel.click_item('TENNIS')
        self.device.driver.execute_script('return performance.mark("HORSERACING_TENNIS_stop");')
        self.device.driver.execute_script('return performance.measure("HORSERACING_TENNIS_navigation", '
                                          '"HORSERACING_TENNIS_start", '
                                          '"HORSERACING_TENNIS_stop");')

    def test_006_navigation_to_golf_page(self):
        """
        DESCRIPTION: Navigate to 'Golf' page
        EXPECTED: 'Golf' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("TENNIS_GOLF_start");')
        self.site.header.brand_logo.click()
        self.site.wait_content_state('Homepage')
        self.site.home.menu_carousel.click_item('GOLF')
        self.device.driver.execute_script('return performance.mark("TENNIS_GOLF_stop");')
        self.device.driver.execute_script('return performance.measure("TENNIS_GOLF_navigation", '
                                          '"TENNIS_GOLF_start", '
                                          '"TENNIS_GOLF_stop");')

    def test_007_navigation_to_cricket_page(self):
        """
        DESCRIPTION: Navigate to 'Cricket' page
        EXPECTED: 'Cricket' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("GOLF_CRICKET_start");')
        self.site.header.brand_logo.click()
        self.site.wait_content_state('Homepage')
        self.site.home.menu_carousel.click_item('CRICKET')
        self.device.driver.execute_script('return performance.mark("GOLF_CRICKET_stop");')
        self.device.driver.execute_script('return performance.measure("GOLF_CRICKET_navigation", '
                                          '"GOLF_CRICKET_start", '
                                          '"GOLF_CRICKET_stop");')

    def test_008_navigation_to_all_sports_page(self):
        """
        DESCRIPTION: Navigate to 'All Sports' page
        EXPECTED: 'All Sports' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("CRICKET_ALLSPORTS_start");')
        self.site.header.brand_logo.click()
        self.site.wait_content_state('Homepage')
        self.site.home.menu_carousel.click_item('ALL SPORTS')
        self.device.driver.execute_script('return performance.mark("CRICKET_ALLSPORTS_stop");')
        self.device.driver.execute_script('return performance.measure("CRICKET_ALLSPORTS_navigation", '
                                          '"CRICKET_ALLSPORTS_start", '
                                          '"CRICKET_ALLSPORTS_stop");')

    def test_009_navigation_to_contact_us_page(self):
        """
        DESCRIPTION: Navigate to 'Contact Us' page
        EXPECTED: 'Contact Us' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("ALLSPORTS_CONTACTUS_start");')
        self.site.login()
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item('Contact Us')
        self.device.driver.execute_script('return performance.mark("ALLSPORTS_CONTACTUS_stop");')
        self.device.driver.execute_script('return performance.measure("ALLSPORTS_CONTACTUS_navigation", '
                                          '"ALLSPORTS_CONTACTUS_start", '
                                          '"ALLSPORTS_CONTACTUS_stop");')
        self.post_to_influxdb()
