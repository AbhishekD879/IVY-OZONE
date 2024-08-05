# coding=utf-8
import pytest

import tests
from test_ui_performance.BasePerformanceTest import BasePerformanceTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
class Test_Football_navigation(BasePerformanceTest, BaseSportTest):
    """
    NAME: Performance test of 'Football' pages navigation
    """
    db_name = 'example3'
    measurement_name = 'Football navigation'
    event = None

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

    def test_002_navigation_to_football_page(self):
        """
        DESCRIPTION: Navigate to 'Football' page
        EXPECTED: 'Football' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_FOOTBALL_start");')
        self.site.home.menu_carousel.click_item('FOOTBALL')
        self.device.driver.execute_script('return performance.mark("HOMEPAGE_FOOTBALL_stop");')
        self.device.driver.execute_script('return performance.measure("HOMEPAGE_FOOTBALL_navigation", '
                                          '"HOMEPAGE_FOOTBALL_start", '
                                          '"HOMEPAGE_FOOTBALL_stop");')

    def test_003_navigation_to_football_coupons_page(self):
        """
        DESCRIPTION: Navigate to 'Football Coupons' page
        EXPECTED: 'Football Coupons' page is navigated
        """
        self.device.driver.execute_script('return performance.mark("FOOTBALL_COUPONS_start");')
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.coupons)
        self.device.driver.execute_script('return performance.mark("FOOTBALL_COUPONS_stop");')
        self.device.driver.execute_script('return performance.measure("FOOTBALL_COUPONS_navigation", '
                                          '"FOOTBALL_COUPONS_start", '
                                          '"FOOTBALL_COUPONS_stop");')

    def test_004_navigation_to_football_competitions_page(self):
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

    def test_005_navigation_to_football_event_details_page(self):
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
        self.site.wait_content_state('CompetitionLeaguePage')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        today_section = sections['Today'] if 'Today' in sections.keys() else None
        events = today_section.items_as_ordered_dict
        self.__class__.event = events[self.event_name] if self.event_name in events.keys() else None
        self.assertTrue(self.event, msg='Could not find event "%s"' % self.event_name)
        self.event.click()
        self.device.driver.execute_script('return performance.mark("COMPETITIONS_EventDetails_stop");')
        self.device.driver.execute_script('return performance.measure("COMPETITIONS_EventDetails_navigation", '
                                          '"COMPETITIONS_EventDetails_start", '
                                          '"COMPETITIONS_EventDetails_stop");')

        self.post_to_influxdb()
