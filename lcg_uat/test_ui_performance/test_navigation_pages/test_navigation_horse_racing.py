# coding=utf-8
import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_Horse_Racing_navigation(BasePerformanceTest, BaseRacing):
    """
    NAME: Performance test of 'Horse Racing' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'Horse Racing navigation'

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

    def test_003_navigation_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' page
        EXPECTED: 'Horse Racing' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("NEXTRACES_HORSERACING_start");')
        self.site.home.menu_carousel.click_item('HORSE RACING')
        self.device.driver.execute_script('return performance.mark("NEXTRACES_HORSERACING_stop");')
        self.device.driver.execute_script('return performance.measure("NEXTRACES_HORSERACING_navigation", '
                                          '"NEXTRACES_HORSERACING_start", '
                                          '"NEXTRACES_HORSERACING_stop");')

    def test_004_navigation_to_horse_racing_tomorrow_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing Tomorrow' page
        EXPECTED: 'Horse Racing Tomorrow' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("HORSERACING_Tomorrow_start");')
        self.site.horse_racing.tabs_menu.click_button('TOMORROW')
        self.device.driver.execute_script('return performance.mark("HORSERACING_Tomorrow_stop");')
        self.device.driver.execute_script('return performance.measure("HORSERACING_Tomorrow_navigation", '
                                          '"HORSERACING_Tomorrow_start", '
                                          '"HORSERACING_Tomorrow_stop");')

    def test_005_navigation_to_horse_racing_future_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing Future' page
        EXPECTED: 'Horse Racing Future' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("Tomorrow_Future_start");')
        self.site.horse_racing.tabs_menu.click_button('FUTURE')
        self.device.driver.execute_script('return performance.mark("Tomorrow_Future_stop");')
        self.device.driver.execute_script('return performance.measure("Tomorrow_Future_navigation", '
                                          '"Tomorrow_Future_start", '
                                          '"Tomorrow_Future_stop");')

    def test_006_navigation_to_horse_racing_event_details_page(self):
        """
        DESCRIPTION: 'Horse Racing Event Details' page is navigated
        EXPECTED: 'Horse Racing Event Details' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("Future_EventDetails_start");')
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                   class_id=self.ob_config.backend.ti.horse_racing.class_ids, brand=self.brand)
        self.__class__.racing_form = ss_req.get_racing_events_to_outcome(next4=True)
        self.open_racing_event(self.racing_form[0]['event']['children'][0]['market']['eventId'])
        sections = self.site.racing_event_details.event_markets_list.items_as_ordered_dict
        section_name, section = sections.items()[0]
        outcomes = section.items_as_ordered_dict
        outcome_name, outcome = outcomes.items()[0]
        outcome.click()
        self.device.driver.execute_script('return performance.mark("Future_EventDetails_stop");')
        self.device.driver.execute_script('return performance.measure("Future_EventDetails_navigation", '
                                          '"Future_EventDetails_start", '
                                          '"Future_EventDetails_stop");')
        self.post_to_influxdb()
