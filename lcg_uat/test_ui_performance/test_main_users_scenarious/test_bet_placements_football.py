# coding=utf-8
import pytest

import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@vtest
class Test_Bet_Placements_Football_navigation(BasePerformanceTest, BaseSportTest, BaseBetSlipTest):
    """
    NAME: Performance test of 'Bet Placements - Football' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'Bet Placements Football navigation'
    event_name = None

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_name = event.team1 + ' v ' + event.team2

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

    def test_006_navigation_to_football_event_details_page(self):
        """
        DESCRIPTION: Navigated created 'Event Details' page
        EXPECTED: 'Event Details' is navigated
        """
        self.device.driver.execute_script('return performance.mark("COMPETITIONS_EventDetails_start");')
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        section = sections['AUTO TEST'] if 'AUTO TEST' in sections.keys() else None
        section.expand()
        wait_for_result(lambda: section.items_as_ordered_dict,
                        name='Leagues list is loaded',
                        timeout=2)
        leagues = section.items_as_ordered_dict
        football_autotest_competition_league = tests.settings.football_autotest_competition_league.title()
        league = leagues[football_autotest_competition_league]
        league.click()
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        today_section = sections['Today'] if 'Today' in sections.keys() else None
        events = today_section.items_as_ordered_dict
        self.__class__.event = events[self.event_name] if self.event_name in events.keys() else None
        self.assertTrue(self.event, msg='Could not find event "%s"' % self.event_name)
        self.event.click()
        output_prices_list = self.site.sport_event_details.tab_content.match_result_market.outcomes.items_as_ordered_dict
        output_prices_list['Draw'].bet_button.click()
        if self.site.wait_for_quick_bet_panel(timeout=2):
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_for_quick_bet_panel(expected_result=False)
            self.site.wait_quick_bet_overlay_to_hide()
        self.device.driver.execute_script('return performance.mark("COMPETITIONS_EventDetails_stop");')
        self.device.driver.execute_script('return performance.measure("COMPETITIONS_EventDetails_navigation", '
                                          '"COMPETITIONS_EventDetails_start", '
                                          '"COMPETITIONS_EventDetails_stop");')

    def test_007_go_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Go to BetSlip and place a bet
        EXPECTED: Place a bet is done
        """
        self.device.driver.execute_script('return performance.mark("EventDetails_PlaceBet_start");')
        self.site.header.bet_slip_counter.click()
        self.place_single_bet()
        self.site.bet_receipt.bet_receipt_sections_list.footer.click_done()
        self.device.driver.execute_script('return performance.mark("EventDetails_PlaceBet_stop");')
        self.device.driver.execute_script('return performance.measure("EventDetails_PlaceBet_navigation", '
                                          '"EventDetails_PlaceBet_start", '
                                          '"EventDetails_PlaceBet_stop");')

    def test_008_navigation_back_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My Bets' page
        EXPECTED: 'My Bets' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("PlaceBet_MYBETS_start");')
        self.site.header.my_bets.click()
        self.device.driver.execute_script('return performance.mark("PlaceBet_MYBETS_stop");')
        self.device.driver.execute_script('return performance.measure("PlaceBet_MYBETS_navigation", '
                                          '"PlaceBet_MYBETS_start", '
                                          '"PlaceBet_MYBETS_stop");')

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
