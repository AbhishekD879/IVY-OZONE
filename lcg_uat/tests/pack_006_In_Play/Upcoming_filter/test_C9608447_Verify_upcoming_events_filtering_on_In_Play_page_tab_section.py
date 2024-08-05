import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.Common import Common
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_sports_ribbon, get_inplay_event_initial_data
from time import sleep
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C9608447_Verify_upcoming_events_filtering_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C9608447
    NAME: Verify upcoming events filtering on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies upcoming events filtering on 'In-Play' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Upcoming events are present in 'Upcoming' section (for mobile/tablet) or when 'Upcoming' switcher is selected (for Desktop)
    PRECONDITIONS: 4. For reaching Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::UPCOMING_EVENT::XXX"
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40808)
    """
    keep_browser_open = True
    true = 'true'
    enable_bs_performance_log = True

    def verify_sport_existence(self, navigate=False):
        sleep(2)
        sport_found = False
        sports = get_inplay_sports_ribbon()
        for sport in sports:
            if sport['categoryId'] != 0 and sport['hasUpcoming'] is True:
                self.__class__.category_id = sport['categoryId']
                self.__class__.sport_url = sport['targetUriCopy']
                sport_found = True
                if navigate:
                    self.navigate_to_page(sport['targetUri'].replace('#/', "").replace("sport/", ""))
                    self.site.wait_content_state_changed(timeout=30)
                break
        self.assertTrue(sport_found, msg='No sports with upcoming events available')

    def verify_event_filtering(self):
        events = get_inplay_event_initial_data(category_id=str(self.category_id))
        for event in events:
            try:
                event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event['id'])[0]['event']
            except SiteServeException:
                continue
            self._logger.info(msg='Event name is' + event_details['name'])
            self.assertIn('M', event_details['siteChannels'],
                          msg='Event attribute siteChannels does not contain "M".')
            self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'],
                          msg=' Flag "EVFLAG_BL" not found')

            is_started = wait_for_result(lambda: 'isStarted' not in [event_details.keys()], timeout=0.5)
            self.assertTrue(is_started, msg=f'attribute "isStarted" is present for "{event_details["name"]}"')

            is_started = wait_for_result(lambda: 'is_off' not in [event_details.keys()], timeout=0.5)
            self.assertTrue(is_started, msg=f'attribute "is_off" is present for "{event_details["name"]}"')
            markets = event_details['children']
            self.assertTrue(markets, msg='Markets not found')
            is_market_bet_in_run = is_resulted = 0
            length = 10 if len(markets) > 11 else len(markets)
            for market in markets[:length]:
                market_details = market['market']
                self.assertIn('M', market_details['siteChannels'],
                              msg='Market attribute siteChannels does not contain "M"'
                                  'in current market' + market_details["templateMarketName"])
                if self.true == market_details.get('isMarketBetInRun'):
                    is_market_bet_in_run += 1
                if 'isResulted' not in market_details.keys():
                    is_resulted += 1
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
            if is_market_bet_in_run < 1:
                raise VoltronException('Event name' + event_details['name'] +
                                       'doesnt have atleast one market with "is_market_bet_in_run" as true.')
            if is_resulted < 1:
                raise VoltronException('Event name' + event_details['name'] +
                                       'doesnt have atleast one market with "is resulted".')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1) Create upcoming events
        """
        if tests.settings.backend_env != 'prod':
            start_time_upcoming = self.get_date_time_formatted_string(hours=10)
            self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True, start_time=start_time_upcoming)
            self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True,
                                                                      start_time=start_time_upcoming)

    def test_001_verify_upcoming_events_within_the_page(self):
        """
        DESCRIPTION: Verify upcoming events within the page
        EXPECTED: All events with next attributes are shown:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Event is NOT started
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        EXPECTED: Events with 'isStarted="true"' and 'is_off'="Y" attributes are NOT present within 'Upcoming' section
        """
        self.navigate_to_page('/in-play')
        self.site.wait_content_state_changed(timeout=30)
        self.verify_sport_existence(navigate=True)
        if self.device_type in ['mobile', 'tablet']:
            grouping_buttons = self.site.inplay.tab_content.items_as_ordered_dict[vec.inplay.UPCOMING_EVENTS_SECTION]
            self.assertTrue(grouping_buttons, msg='"In-play" tab contents are not available ')
            sports = list(grouping_buttons.items_as_ordered_dict.values())
            self.site.contents.scroll_to_top()
            sports[0].click()
        else:
            grouping_buttons = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict[
                vec.inplay.UPCOMING_SWITCHER]
            grouping_buttons.click()
        sleep(3)
        self.verify_event_filtering()

    def test_002_repeat_step_1_on_home_page__in_play_tab_for_mobiletablet_sports_landing_page__in_play_tab(self):
        """
        DESCRIPTION: Repeat step 1 on:
        DESCRIPTION: * Home page > 'In-Play' tab **For Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('/home/in-play')
            self.site.wait_content_state_changed(timeout=10)
            self.site.home.tabs_menu.click_button('IN-PLAY')
            self.site.wait_content_state_changed(timeout=10)
            self.verify_sport_existence()
            upcoming = list(self.site.home.tab_content.upcoming.items_as_ordered_dict.values())
            upcoming[0].click()
            sleep(3)
            self.verify_event_filtering()
        self.verify_sport_existence()
        self.navigate_to_page(self.sport_url + '/live')
        self.site.wait_content_state_changed(timeout=30)
        if self.device_type in ['mobile', 'tablet']:
            sleep(2)
            grouping_buttons = self.site.inplay.tab_content.upcoming
            self.assertTrue(grouping_buttons, msg='"In-play" tab contents are not available ')
            sports = list(grouping_buttons.items_as_ordered_dict.values())
            self.site.contents.scroll_to_top()
            sports[0].click()
        else:
            grouping_buttons = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict[
                vec.inplay.UPCOMING_SWITCHER]
            grouping_buttons.click()
        sleep(3)
        self.verify_event_filtering()
