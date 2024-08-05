# coding=utf-8
import pytest

from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_Double_Bet_Horse_Racing_navigation(BasePerformanceTest, BaseRacing, BaseBetSlipTest):
    """
    NAME: Performance test of 'Double Bet Horse Racing' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'Double Bet Horse racing'
    event_ids_1, event_ids_2 = None, None

    def test_000_create_racing_events(self):
        """
        DESCRIPTION: Create racing events with Each Way terms available
        EXPECTED: Racing events with Each Way terms are created
        """
        event_parameters_1 = self.ob_config.add_UK_racing_event()
        self.__class__.event_ids_1 = event_parameters_1.event_id
        event_parameters_2 = self.ob_config.add_UK_racing_event()
        self.__class__.event_ids_2 = event_parameters_2.event_id

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

    def test_006_first_navigation_to_event_details_page_and_adding_first_selection_to_betslip(self):
        """
        DESCRIPTION: First navigation to 'Event Details' page and add first selection to BetSlip
        EXPECTED: 'Event Details' page is navigated
        EXPECTED: Selection is added to BetSlip
        """
        self.device.driver.execute_script('return performance.mark("Future_AddFirstSelection_start");')
        self.open_racing_event(eventID=self.event_ids_1)
        sections = self.site.racing_event_details.event_markets_list.items_as_ordered_dict
        section_name, section = sections.items()[0]
        outcomes = section.items_as_ordered_dict
        outcome = next((outcome for outcome in outcomes.values() if outcome.bet_button.is_enabled()), None)
        outcome.bet_button.click()
        if self.site.wait_for_quick_bet_panel(timeout=2):
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_for_quick_bet_panel(expected_result=False)
            self.site.wait_quick_bet_overlay_to_hide()
        self.device.driver.execute_script('return performance.mark("Future_AddFirstSelection_stop");')
        self.device.driver.execute_script('return performance.measure("Future_AddFirstSelection_navigation", '
                                          '"Future_AddFirstSelection_start", '
                                          '"Future_AddFirstSelection_stop");')

    def test_007_second_navigation_to_event_details_page_and_adding_second_selection_to_betslip(self):
        """
        DESCRIPTION: Second navigation to 'Event Details' page and add second selection to BetSlip
        EXPECTED: 'Event Details' page is navigated
        EXPECTED: Selection is added to BetSlip
        """
        self.device.driver.execute_script('return performance.mark("Future_AddSecondSelection_start");')
        self.open_racing_event(eventID=self.event_ids_2)
        sections = self.site.racing_event_details.event_markets_list.items_as_ordered_dict
        section_name, section = sections.items()[0]
        outcomes = section.items_as_ordered_dict
        outcome = next((outcome for outcome in outcomes.values() if outcome.bet_button.is_enabled()), None)
        outcome.bet_button.click()
        self.device.driver.execute_script('return performance.mark("Future_AddSecondSelection_stop");')
        self.device.driver.execute_script('return performance.measure("Future_AddSecondSelection_navigation", '
                                          '"Future_AddSecondSelection_start", '
                                          '"Future_AddSecondSelection_stop");')

    def test_008_navigation_to_betslip(self):
        """
        DESCRIPTION: Navigate to 'Betslip'
        EXPECTED: 'Betslip' navigated
        """
        self.device.driver.execute_script('return performance.mark("AddSecondSelection_Betslip_start");')
        self.site.header.bet_slip_counter.click()
        self.device.driver.execute_script('return performance.mark("AddSecondSelection_Betslip_stop");')
        self.device.driver.execute_script('return performance.measure("AddSecondSelection_Betslip_navigation", '
                                          '"AddSecondSelection_Betslip_start", '
                                          '"AddSecondSelection_Betslip_stop");')

    def test_009_placing_double_bets(self):
        """
        DESCRIPTION: Place Double bets
        EXPECTED: Double bets placed
        """
        self.device.driver.execute_script('return performance.mark("Betslip_PlaceDoubleBets_start");')
        self.place_multiple_bet()
        self.device.driver.execute_script('return performance.mark("Betslip_PlaceDoubleBets_stop");')
        self.device.driver.execute_script('return performance.measure("Betslip_PlaceDoubleBets_navigation", '
                                          '"Betslip_PlaceDoubleBets_start", '
                                          '"Betslip_PlaceDoubleBets_stop");')

    def test_010_navigation_to_logout_page(self):
        """
        DESCRIPTION: Perform 'Logout'
        EXPECTED: 'Logout' is performed
        """
        self.device.driver.execute_script('return performance.mark("PlaceDoubleBets_LOGOUT_start");')
        self.site.bet_receipt.bet_receipt_sections_list.footer.click_done()
        self.site.logout()
        self.device.driver.execute_script('return performance.mark("PlaceDoubleBets_LOGOUT_stop");')
        self.device.driver.execute_script('return performance.measure("PlaceDoubleBets_LOGOUT_navigation", '
                                          '"PlaceDoubleBets_LOGOUT_start", '
                                          '"PlaceDoubleBets_LOGOUT_stop");')
        self.post_to_influxdb()
