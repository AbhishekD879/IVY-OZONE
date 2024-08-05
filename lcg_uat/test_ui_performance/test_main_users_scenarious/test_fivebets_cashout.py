# coding=utf-8
import pytest

import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.cash_out
@vtest
class Test_Five_Bets_Cashout_navigation(BasePerformanceTest, BaseSportTest):
    """
    NAME: Performance test of 'Five Bets Cashout' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'Five Bets Cashout navigation'
    betslip_selection_names_attempt1 = []
    betslip_selection_names_attempt2 = []
    selection_ids_1 = None
    selection_ids_2 = None
    selection_ids_3 = None
    selection_ids_4 = None
    selection_ids_5 = None
    first_selection = None
    second_selection = None
    third_selection = None
    fourth_selection = None
    fifth_selection = None

    def place_multiple_bet(self, attempt=1):
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        for stake_name in singles_section.keys():
            self.__class__.betslip_selection_names_attempt1.append(singles_section[stake_name].outcome_name) if attempt == 1 else\
                self.__class__.betslip_selection_names_attempt2.append(singles_section[stake_name].outcome_name)
        for stake_name in multiples_section.keys():
            multiples_section[stake_name].amount_form.input.value = self.bet_amount
            self.__class__.betslip_selection_names_attempt1.append(multiples_section[stake_name].outcome_name) if attempt == 1 else\
                self.__class__.betslip_selection_names_attempt2.append(multiples_section[stake_name].outcome_name)
            self.assertEqual(self.bet_amount, float(multiples_section[stake_name].amount_form.input.value),
                             msg='The value of %s is not present in the \'Stake\' field, the value is: %s'
                             % (self.bet_amount, multiples_section[stake_name].amount_form.input.value))

        betnow_section = self.get_betslip_content().betnow_section
        betnow_section.bet_now_button.click()

    def test_000_create_events_and_login(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Login as user that have enough money to place bet
        """
        eventID, self.__class__.first_selection, team2, self.__class__.selection_ids_1 = \
            self.ob_config.add_autotest_premier_league_football_event()
        eventID, self.__class__.second_selection, team2, self.__class__.selection_ids_2 = \
            self.ob_config.add_autotest_premier_league_football_event()
        eventID, self.__class__.third_selection, team2, self.__class__.selection_ids_3 = \
            self.ob_config.add_autotest_premier_league_football_event()
        eventID, self.__class__.fourth_selection, team2, self.__class__.selection_ids_4 = \
            self.ob_config.add_autotest_premier_league_football_event()
        eventID, self.__class__.fifth_selection, team2, self.__class__.selection_ids_5 = \
            self.ob_config.add_autotest_premier_league_football_event()

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
        self.open_betslip_with_selections(selection_ids=(self.selection_ids_1[self.first_selection],
                                                         self.selection_ids_2[self.second_selection],
                                                         self.selection_ids_3[self.third_selection],
                                                         self.selection_ids_4[self.fourth_selection],
                                                         self.selection_ids_5[self.fifth_selection]))
        self.device.driver.execute_script('return performance.mark("COMPETITIONS_SelectEvents_stop");')
        self.device.driver.execute_script('return performance.measure("COMPETITIONS_SelectEvents_navigation", '
                                          '"COMPETITIONS_SelectEvents_start", '
                                          '"COMPETITIONS_SelectEvents_stop");')

    def test_007_go_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Go to BetSlip and place a bet
        EXPECTED: Place a bet is done
        """
        self.device.driver.execute_script('return performance.mark("SelectEvents_PlaceBet_start");')
        self.place_multiple_bet()
        self.site.bet_receipt.bet_receipt_sections_list.footer.click_done()
        self.device.driver.execute_script('return performance.mark("SelectEvents_PlaceBet_stop");')
        self.device.driver.execute_script('return performance.measure("SelectEvents_PlaceBet_navigation", '
                                          '"SelectEvents_PlaceBet_start", '
                                          '"SelectEvents_PlaceBet_stop");')

    def test_008_navigation_to_my_bets_and_perform_cashout(self):
        """
        DESCRIPTION: Navigate to 'My Bets' and perform 'Cashout'
        EXPECTED: 'My Bets' page is navigated
        EXPECTED: 'Cashout' is performed
        """
        self.device.driver.execute_script('return performance.mark("PlaceBet_MYBETS_start");')
        self.site.open_my_bets_cashout()
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')
        bet = list(bets.items_as_ordered_dict.items())[0]
        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()

    def test_009_navigation_to_logout_page(self):
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
