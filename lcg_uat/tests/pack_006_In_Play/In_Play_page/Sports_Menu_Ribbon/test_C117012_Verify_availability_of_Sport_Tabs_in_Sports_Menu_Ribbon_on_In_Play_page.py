import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.helpers import get_inplay_sports_ribbon, get_inplay_event_initial_data, get_inplay_sports_ribbon_home_page
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C117012_Verify_availability_of_Sport_Tabs_in_Sports_Menu_Ribbon_on_In_Play_page(Common):
    """
    TR_ID: C117012
    NAME: Verify availability of Sport Tabs in Sports Menu Ribbon on 'In-Play' page
    DESCRIPTION: This test case verifies conditions under which Sport Tabs are displayed in Sports Menu Ribbon on 'In-Play' page
    DESCRIPTION: To be run on Mobile, Tablet and Desktop.
    PRECONDITIONS: 1) To get Sports which have 'Live Now' events:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:intersects:16,34,51,5,6,24,18,22,31,30,32,23,55,26,28,25,1,9,10,13,48,46,20,3,54,36,8,35,12,42,53,21,19,39,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149,16,34,51,6,18,9,20,54,36,12,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149&existsFilter=class:simpleFilter:event.drilldownTagNames:intersects:EVFLAG_BL&existsFilter=class:simpleFilter:event.siteChannels:contains:M&simpleFilter=class.siteChannels:contains:M&existsFilter=class:simpleFilter:event.isLiveNowEvent&simpleFilter=class.hasLiveNowEvent&translationLang=LL
    PRECONDITIONS: 2) To get Sports which have 'Upcoming' events:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.22/Class?simpleFilter=class.categoryId:intersects:16,34,51,5,6,24,18,22,31,30,32,23,55,26,28,25,1,9,10,13,48,46,20,3,54,36,8,35,12,42,53,21,19,39,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149,16,34,51,6,18,9,20,54,36,12,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149&existsFilter=class:simpleFilter:event.drilldownTagNames:intersects:EVFLAG_BL&existsFilter=class:simpleFilter:event.siteChannels:contains:M&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasNext24HourEvent&existsFilter=class:simpleFilter:event.isNext24HourEvent&translationLang=LL
    PRECONDITIONS: 3) To get events for particular class ID:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.22/EventToOutcomeForClass/XXX?&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXX - class ID
    """
    keep_browser_open = True
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
        """
        if tests.settings.backend_env != 'prod':
            start_time_upcoming = self.get_date_time_formatted_string(hours=10)
            self.ob_config.add_autotest_premier_league_football_event(is_live=True, perform_stream=True)
            self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True,
                                                                      start_time=start_time_upcoming)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("Home")

    def test_002_for_mobiletablettap_in_play_icon_on_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: *   'In-Play' Landing Page is opened
        EXPECTED: *   Sports Menu Ribbon is shown with Categories where In-Play events are available
        EXPECTED: *   First <Sport> tab is opened by default
        EXPECTED: *   Two filter switchers are visible: 'Live Now' and 'Upcoming'
        """
        if self.device_type == 'mobile':
            try:
                self.site.home.menu_carousel.click_item(vec.siteserve.IN_PLAY_TAB)
            except VoltronException:
                self.site.home.menu_carousel.click_item(vec.SB.ALL_SPORTS)
                self.site.all_sports.click_item(vec.SB.IN_PLAY)
            self.site.wait_content_state(state_name='in-play', timeout=30)
            live_now = self.site.inplay.tab_content.live_now
            upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(live_now.is_displayed(), msg=f'"{vec.inplay.LIVE_NOW_SWITCHER}"is not visible')
            self.assertTrue(upcoming.is_displayed(), msg=f'"{vec.inplay.UPCOMING_SWITCHER}"is not visible')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='"menu items" are not found')
            in_play_tab = menu_items[vec.siteserve.IN_PLAY_TAB]
            in_play_tab.click()
            self.site.wait_content_state(state_name='in-play')
            sections = list(self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.keys())
            expected_sections = [vec.Inplay.LIVE_NOW_SWITCHER, vec.Inplay.UPCOMING_SWITCHER]
            self.assertEqual(sections, expected_sections,
                             msg=f'Actual sections:"{sections}"are not same as Expected sections:"{expected_sections}"')
        self.__class__.sports_categories = list(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.values())
        self.assertTrue(self.sports_categories, msg='"sports Categories" are not displayed')
        first_sport = self.sports_categories[1]
        self.assertTrue(first_sport.is_selected(), msg=f'"{first_sport.name}" tab is not opened by default')

    def test_003_for_mobiletabletverify_sport_tabs_filtering(self):
        """
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: Verify Sport tabs filtering
        EXPECTED: Each unique Sport Tab is displayed in Sports Menu Ribbon only if at least one class for the corresponding category has the following attributes:
        EXPECTED: *   Class's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Class's attribute hasLiveNowEvent="true" OR hasNext24HourEvent="true"
        EXPECTED: *   At least one event in the class has attribute 'siteChannels' that contains 'M'
        EXPECTED: *   At least one event in the class contains attribute drilldownTagNames="EVFLAG_BL"
        EXPECTED: *   At least one event in the class contains attribute isLiveNowEvent="true" OR isNext24HourEvent="true"
        """
        if self.device_type == 'mobile':
            parameters = get_inplay_sports_ribbon()
            self.assertTrue(parameters, msg='There are no events in inplay page')
            num_of_sports = 4 if len(parameters) - 1 > 4 else len(parameters) - 1
            for sport in parameters[1:num_of_sports]:
                category_id = str(sport['categoryId'])
                live_or_upcoming = True if sport['hasLiveNow'] is True or sport['hasUpcoming'] is True else False
                self.assertTrue(live_or_upcoming,
                                msg='Class attribute does not have hasLiveNowEvent OR hasUpcomingEvent = true attributes')
                menu_items = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
                self.assertTrue(menu_items, msg='No Sports Menu Ribbon in "In-play"')
                if self.brand == 'ladbrokes':
                    menu_items[sport['categoryName'].replace("_", " ")].click()
                else:
                    menu_items[sport['categoryCode'].replace("_", " ")].click()
                self.site.wait_splash_to_hide()
                sleep(3)
                events = get_inplay_event_initial_data(category_id=category_id)
                try:
                    self.assertTrue(events, msg=f'No events found for the category "{sport["categoryName"]}"')
                except Exception:
                    if self.device_type == 'mobile':
                        grouping_buttons = self.site.inplay.tab_content.items_as_ordered_dict[
                            vec.inplay.UPCOMING_EVENTS_SECTION]
                        self.assertTrue(grouping_buttons, msg='"In-play" tab contents are not available ')
                        sports = list(grouping_buttons.items_as_ordered_dict.values())
                        self.site.contents.scroll_to_top()
                        sports[0].click()
                    else:
                        grouping_buttons = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict[vec.inplay.UPCOMING_SWITCHER]
                        grouping_buttons.click()
                    sleep(3)
                    events = get_inplay_event_initial_data(category_id=category_id)
                event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=events[0]['id'])[0]['event']
                self._logger.info(msg='Event name is' + event_details['name'])
                self.assertIn('M', event_details['siteChannels'], msg=f'Event attribute siteChannels does not contain "M" for "{event_details["name"]}"')
                self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'],
                              msg=f' Flag "EVFLAG_BL" not found for "{event_details["name"]}"')
                result = event_details.get('isLiveNowEvent') or event_details.get('isLiveNowOrFutureEvent')
                self.assertTrue(result,
                                msg='At least one event in the class does not contain attribute isLiveNowEvent="true" OR IsUpcomingEvent="true"')
                markets = event_details['children']
                self.assertTrue(markets, msg='Markets not found')
                for market in markets:
                    market_details = market['market']
                    self.assertIn('M', market_details['siteChannels'],
                                  msg='Market attribute siteChannels does not contain "M"'
                                  'in current market' + market_details["templateMarketName"])
                    try:
                        outcomes = market_details['children']
                    except KeyError:
                        self._logger.info(
                            'current market' + market_details["templateMarketName"] + ' does not have outcomes')
                        continue
                    if outcomes:
                        for outcome in outcomes:
                            outcome_details = outcome['outcome']
                            self.assertIn('M', outcome_details['siteChannels'],
                                          msg='Outcome attribute siteChannels does not contain "M".')

    def test_004_for_desktopnavigate_to_in_play__live_stream_section_on_homepage_and_verify_sport_tabs_filtering(self):
        """
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage and verify Sport tabs filtering
        EXPECTED: Each unique Sport Tab is displayed in Sports Menu Ribbon only if at least one class for the corresponding category has the following attributes:
        EXPECTED: *   Class's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Class's attribute hasLiveNowEvent="true"
        EXPECTED: *   At least one event in the class has attribute 'siteChannels' that contains 'M'
        EXPECTED: *   At least one event in the class contains attribute drilldownTagNames="EVFLAG_BL"
        EXPECTED: *   At least one event in the class contains attribute isLiveNowEvent="true"
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            menu_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No sport items found in In-play and live stream')

            parameters = get_inplay_sports_ribbon_home_page()
            num_of_sports = len(parameters) - 1
            for sport in parameters[:num_of_sports]:
                category_id = str(sport['categoryId'])
                self.assertTrue(sport['hasLiveNow'],
                                msg='Class attribute has no hasLiveNowEvent="true" attribute')
                if self.brand == 'ladbrokes':
                    menu_items[sport['categoryName'].replace("_", " ")].click()
                else:
                    menu_items[sport['categoryCode'].replace("_", " ")].click()
                self.site.wait_splash_to_hide()
                sleep(3)
                events = get_inplay_event_initial_data(category_id=category_id)
                self.assertTrue(events, msg=f'No events found for the category "{sport["categoryName"]}"')
                event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=events[0]['id'])[0]['event']
                self._logger.info(msg='Event name is' + event_details['name'])
                self.assertIn('M', event_details['siteChannels'],
                              msg=f'Event attribute siteChannels does not contain "M" for "{event_details["name"]}"')
                self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'],
                              msg=f' Flag "EVFLAG_BL" not found for "{event_details["name"]}"')
                self.assertTrue(event_details['isLiveNowEvent'],
                                msg='At least one event in the class does not contain attribute isLiveNowEvent="true"')
                markets = event_details['children']
                self.assertTrue(markets, msg='Markets not found')
                for market in markets:
                    market_details = market['market']
                    self.assertIn('M', market_details['siteChannels'],
                                  msg='Market attribute siteChannels does not contain "M"'
                                      'in current market' + market_details["templateMarketName"])
                    try:
                        outcomes = market_details['children']
                    except KeyError:
                        self._logger.info(
                            'current market' + market_details["templateMarketName"] + ' does not have outcomes')
                        continue
                    if outcomes:
                        for outcome in outcomes:
                            outcome_details = outcome['outcome']
                            self.assertIn('M', outcome_details['siteChannels'],
                                          msg='Outcome attribute siteChannels does not contain "M".')
