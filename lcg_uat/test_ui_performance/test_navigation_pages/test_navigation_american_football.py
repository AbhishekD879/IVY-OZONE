# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_American_Football_navigation(BasePerformanceTest):
    """
    NAME: Performance test of 'American Football' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'American football navigation'

    def test_001_load_home_page(self):
        """
        DESCRIPTION: Load 'Home' page
        EXPECTED: 'Home' page is loaded
        """
        self.navigate_to_url(self.test_hostname)

    def test_002_navigation_to_all_sports_page(self):
        """
        DESCRIPTION: Navigate to 'All Sports' page
        EXPECTED: 'All Sports' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_ALLSPORTS_start");')
        self.site.home.menu_carousel.click_item('ALL SPORTS')
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_ALLSPORTS_stop");')
        self.device.driver.execute_script('return performance.measure("HOMEPAGE_ALLSPORTS_navigation", '
                                          '"HOMEPAGE_ALLSPORTS_start", '
                                          '"HOMEPAGE_ALLSPORTS_stop");')

    def test_003_navigation_to_american_football_page(self):
        """
        DESCRIPTION: Navigate to 'American Football' page
        EXPECTED: 'American Football' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("ALLSPORTS_AMERICANFOOTBALL_start");')
        self.site.home.menu_carousel.click_item('AMERICAN FOOTBALL')
        self.device.driver.execute_script('return performance.mark("ALLSPORTS_AMERICANFOOTBALL_stop");')
        self.device.driver.execute_script('return performance.measure("ALLSPORTS_AMERICANFOOTBALL_navigation", '
                                          '"ALLSPORTS_AMERICANFOOTBALL_start", '
                                          '"ALLSPORTS_AMERICANFOOTBALL_stop");')
        self.post_to_influxdb()
