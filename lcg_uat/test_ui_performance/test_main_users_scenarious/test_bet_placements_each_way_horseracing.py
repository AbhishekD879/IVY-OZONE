# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_Bet_Placements_Eachway_Bet_Horse_Racing_navigation(BasePerformanceTest, BaseRacing, BaseBetSlipTest):
    """
    NAME: Performance test of 'Bet Placements Each-way Bet Horse Racing' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'Bet Horse Racing navigation'
    eventIDs = {}
    expected_ew_terms = {'ew_places': 3, 'ew_fac_num': 1, 'ew_fac_den': 6}
    ew_terms = ''

    def test_000_create_racing_event(self):
        """
        DESCRIPTION: Create racing event with Each Way terms
        EXPECTED: Racing event with Each Way terms created
        """
        self.__class__.eventIDs.update({'ew_available': self.ob_config.add_UK_racing_event(
            ew_terms=self.expected_ew_terms,
            time_to_start=10)[0]})
        self._logger.info('*** Created events with IDs %s' % self.eventIDs)

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

    def test_004_navigation_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' page
        EXPECTED: 'Horse Racing' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("LOGIN_HORSERACING_start");')
        self.site.home.menu_carousel.click_item('HORSE RACING')
        self.device.driver.execute_script('return performance.mark("LOGIN_HORSERACING_stop");')
        self.device.driver.execute_script('return performance.measure("LOGIN_HORSERACING_navigation", '
                                          '"LOGIN_HORSERACING_start", '
                                          '"LOGIN_HORSERACING_stop");')

    def test_005_navigation_to_horse_racing_future_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing Future' page
        EXPECTED: 'Horse Racing Future' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("HORSERACING_Future_start");')
        self.site.horse_racing.tabs_menu.click_button('FUTURE')
        self.device.driver.execute_script('return performance.mark("HORSERACING_Future_stop");')
        self.device.driver.execute_script('return performance.measure("HORSERACING_Future_navigation", '
                                          '"HORSERACING_Future_start", '
                                          '"HORSERACING_Future_stop");')

    def test_006_navigate_to_the_event_details_page(self):
        """
        DESCRIPTION: Navigate to the event details page
        EXPECTED: 1. Event details page is opened
        EXPECTED: 2. 'Win or E/W' tab is opened by default
        """
        self.device.driver.execute_script('return performance.mark("Future_AddSelection_start");')
        self.open_racing_event(eventID=self.eventIDs['ew_available'])
        sections = self.site.racing_event_details.event_markets_list.items_as_ordered_dict
        section_name, section = sections.items()[0]
        outcomes = section.items_as_ordered_dict
        outcome = next((outcome for outcome in outcomes.values() if outcome.bet_button.is_enabled()), None)
        outcome.bet_button.click()
        if self.site.wait_for_quick_bet_panel(timeout=2):
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_for_quick_bet_panel(expected_result=False)
            self.site.wait_quick_bet_overlay_to_hide()
        self.device.driver.execute_script('return performance.mark("Future_AddSelection_stop");')
        self.device.driver.execute_script('return performance.measure("Future_AddSelection_navigation", '
                                          '"Future_AddSelection_start", '
                                          '"Future_AddSelection_stop");')

    def test_007_click_each_way_place_bet_checkbox(self):
        """
        DESCRIPTION: Click 'Each Way' place bet checkbox
        EXPECTED: 'Each Way' place bet checkbox is clicked
        """
        self.device.driver.execute_script('return performance.mark("AddSelection_EachWay_start");')
        self.site.header.bet_slip_counter.click()
        self.place_single_bet(number_of_stakes=1, each_way=True)
        self.site.bet_receipt.bet_receipt_sections_list.footer.click_done()
        self.device.driver.execute_script('return performance.mark("AddSelection_EachWay_stop");')
        self.device.driver.execute_script('return performance.measure("AddSelection_EachWay_navigation", '
                                          '"AddSelection_EachWay_start", '
                                          '"AddSelection_EachWay_stop");')

    def test_008_navigation_to_logout_page(self):
        """
        DESCRIPTION: Perform 'Logout'
        EXPECTED: 'Logout' is performed
        """
        self.device.driver.execute_script('return performance.mark("EachWay_LOGOUT_start");')
        self.site.logout()
        self.device.driver.execute_script('return performance.mark("EachWay_LOGOUT_stop");')
        self.device.driver.execute_script('return performance.measure("EachWay_LOGOUT_navigation", '
                                          '"EachWay_LOGOUT_start", '
                                          '"EachWay_LOGOUT_stop");')
        self.post_to_influxdb()
