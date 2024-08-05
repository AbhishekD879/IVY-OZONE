# coding=utf-8
import pytest

import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_My_ACCA_Bet_navigation(BasePerformanceTest, BaseSportTest, BaseBetSlipTest):
    """
    NAME: Performance test of 'My ACCA Bet' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'My ACCA Bet'
    prices = {
        'odds_home': '5/1',
        'odds_draw': '3/2',
        'odds_away': '4/1',
    }
    selection_ids_1 = {}
    selection_ids_2 = {}
    selection_ids_3 = {}

    def test_000_create_events(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        eventID1, self.__class__.team1_1, self.__class__.team2_1, self.__class__.selection_ids_1 = \
            self.ob_config.add_football_event_to_autotest_league2(lp=self.prices)
        eventID2, self.__class__.team1_2, self.__class__.team2_2, self.__class__.selection_ids_2 = \
            self.ob_config.add_football_event_to_autotest_league2(lp=self.prices)
        eventID3, self.__class__.team1_3, self.__class__.team2_3, self.__class__.selection_ids_3 = \
            self.ob_config.add_football_event_to_autotest_league2(lp=self.prices)

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
        DESCRIPTION: Perform 'Login' as user that have enough money to place bet
        EXPECTED: 'Login' is performed
        """
        self.device.driver.execute_script('return performance.mark("NEXTRACES_LOGIN_start");')
        self.site.login(username=tests.settings.betplacement_user)
        self.device.driver.execute_script('return performance.mark("NEXTRACES_LOGIN_stop");')
        self.device.driver.execute_script('return performance.measure("NEXTRACES_LOGIN_navigation", '
                                          '"NEXTRACES_LOGIN_start", '
                                          '"NEXTRACES_LOGIN_stop");')

    def test_004_navigation_to_football_page(self):
        """
        DESCRIPTION: Navigate to 'Football' page
        EXPECTED: 'Football' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("LOGIN_FOOTBALL_start");')
        self.site.home.menu_carousel.click_item('FOOTBALL')
        self.device.driver.execute_script('return performance.mark("LOGIN_FOOTBALL_stop");')
        self.device.driver.execute_script('return performance.measure("LOGIN_FOOTBALL_navigation", '
                                          '"LOGIN_FOOTBALL_start", '
                                          '"LOGIN_FOOTBALL_stop");')

    def test_005_navigation_to_football_competitions_page(self):
        """
        DESCRIPTION: Navigate to 'Football Competitions' page
        EXPECTED: 'Football Competitions' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("FOOTBALL_COMPETITIONS_start");')
        self.site.football.tabs_menu.click_button('COMPETITIONS')
        self.device.driver.execute_script('return performance.mark("FOOTBALL_COMPETITIONS_stop");')
        self.device.driver.execute_script('return performance.measure("FOOTBALL_COMPETITIONS_navigation", '
                                          '"FOOTBALL_COMPETITIONS_start", '
                                          '"FOOTBALL_COMPETITIONS_stop");')

    def test_006_selecting_five_events_to_betslip_page(self):
        """
        DESCRIPTION: Selecting five events to Betslip page
        EXPECTED: Five events are selected
        """
        self.device.driver.execute_script('return performance.mark("COMPETITIONS_SelectEvents_start");')
        selection1_name, selection1_id = self.selection_ids_1.items()[0]
        selection2_name, selection2_id = self.selection_ids_2.items()[1]
        selection3_name, selection3_id = self.selection_ids_3.items()[2]
        self.open_betslip_with_selections(selection_ids=(selection1_id, selection2_id, selection3_id))
        self.device.driver.execute_script('return performance.mark("COMPETITIONS_SelectEvents_stop");')
        self.device.driver.execute_script('return performance.measure("COMPETITIONS_SelectEvents_navigation", '
                                          '"COMPETITIONS_SelectEvents_start", '
                                          '"COMPETITIONS_SelectEvents_stop");')

    def test_007_go_to_betslip_and_place_acca_bet(self):
        """
        DESCRIPTION: Go to BetSlip and place an ACCA bet
        EXPECTED: Place an ACCA bet is done
        """
        self.device.driver.execute_script('return performance.mark("SelectEvents_ACCABet_start");')
        self.place_multiple_bet(acca=True)
        self.site.bet_receipt.bet_receipt_sections_list.footer.click_done()
        self.device.driver.execute_script('return performance.mark("SelectEvents_ACCABet_stop");')
        self.device.driver.execute_script('return performance.measure("SelectEvents_ACCABet_navigation", '
                                          '"SelectEvents_ACCABet_start", '
                                          '"SelectEvents_ACCABet_stop");')

    def test_008_navigation_to_logout_page(self):
        """
        DESCRIPTION: Perform 'Logout'
        EXPECTED: 'Logout' is performed
        """
        self.device.driver.execute_script('return performance.mark("ACCABet_LOGOUT_start");')
        self.site.logout()
        self.device.driver.execute_script('return performance.mark("ACCABet_LOGOUT_stop");')
        self.device.driver.execute_script('return performance.measure("ACCABet_LOGOUT_navigation", '
                                          '"ACCABet_LOGOUT_start", '
                                          '"ACCABet_LOGOUT_stop");')
        self.post_to_influxdb()
