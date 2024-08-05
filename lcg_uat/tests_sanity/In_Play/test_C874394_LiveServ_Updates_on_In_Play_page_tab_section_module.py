from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live updates cannot be tested on prod and hl
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@vtest
class Test_C874394_LiveServ_Updates_on_In_Play_page_tab_section_module(BaseFeaturedTest):
    """
    TR_ID: C874394
    NAME: LiveServ Updates on 'In-Play' page/tab/section/module [HL/TEST2]
    DESCRIPTION: This test case verifies LiveServ updates on 'In-Play' page/tab/section/module
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page > <Sports> tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) Live event should contain the following attributes:
    PRECONDITIONS: * "rawIsOffCode" : "Y"
    PRECONDITIONS: * "isStarted" : "true"
    PRECONDITIONS: * "drilldownTagNames" : "EVFLAG_BL"
    PRECONDITIONS: * "isMarketBetInRun: : "true"
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To get SiteServer info about the event please use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: 2) To verify price updates check new received values in "lp_den" and "lp_num" attributes using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: PRICE
    PRECONDITIONS: 3) To verify suspension/unsuspension check new received values in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCT depends on level of triggering the status changes (event/market/outcome)
    """
    keep_browser_open = True
    new_price = '1/7'

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.device_type == 'mobile' and tests.settings.cms_env != 'prd0':
            cms_config = cls.get_cms_config()
            if cls.in_play_event_count is not None:
                cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)
            if cls.sport_number is not None and cls.sport_event_count is not None:
                cms_config.update_inplay_sport_event_count(sport_number=cls.sport_number,
                                                           event_count=cls.sport_event_count)

    def get_price_button(self, event):
        price_buttons = event.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')
        _, price_button = list(price_buttons.items())[0]
        return price_button

    def check_event_odds_state(self, event, level, expected_result=True, timeout=30):
        """
        Verifies state of price buttons
        :param event: specifies the event object
        :param level: level on which status change was made in Backoffice e.g. 'event', 'market', 'selection'
        :param expected_result: specifies expected result. True if buttons should be enabled, False otherwise
        :param timeout: time to wait for button status change
        :return: True if price buttons' state matches expected value
        """
        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')

        if expected_result:
            for button_name, button in price_buttons:
                result = button.is_enabled(timeout=timeout, expected_result=expected_result)
                self.assertTrue(result, msg=f'Price button "{button_name}" was not enabled')
        else:
            if level == 'event' or level == 'market':
                for button_name, button in price_buttons:
                    result = button.is_enabled(timeout=timeout, expected_result=expected_result)
                    self.assertFalse(result, msg=f'Price button "{button_name}" was not disabled')
            elif level == 'selection':
                button_name, button = price_buttons[0]
                result = button.is_enabled(timeout=timeout, expected_result=expected_result)
                self.assertFalse(result, msg=f'Price button "{button_name}" was not disabled')

                for button_name, button in price_buttons[1:]:
                    result = button.is_enabled(timeout=timeout, expected_result=not expected_result)
                    self.assertTrue(result, msg=f'Price button "{button_name}" was disabled after another selection suspended')
            else:
                raise VoltronException('Please specify correct level: event, market or selection')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live now and upcoming events
        DESCRIPTION: 1. Load the app
        DESCRIPTION: 2. Navigate to the 'In-Play' page > <Sports> tab
        """
        self.__class__.widget_section_name = 'In-Play LIVE Football'
        self.__class__.sport_name = self.get_sport_title(category_id=self.ob_config.football_config.category_id).upper()

        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, img_stream=True)
        self.__class__.eventID = event_params.event_id
        self.__class__.live_event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.live_now_selection_id = list(event_params.selection_ids.values())[0]
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, raise_exceptions=False)

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=resp[0], in_play_page_sport_tab=True)
        self.__class__.ui_section_name = self.section_name if self.brand == 'ladbrokes' else self.section_name.title()

        self.__class__.module_title = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                              id=self.eventID)['title'].upper()

        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                            in_play_tab_home_page=True)

        self.__class__.league_name_in_play_live_watch_live = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                       in_play_page_watch_live=True)
        self.check_sport_presence_on_inplay(sport_name='/football')
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        football_tab = vec.siteserve.FOOTBALL_TAB.title() if self.brand == 'ladbrokes' else vec.siteserve.FOOTBALL_TAB.upper()

        self.site.inplay.inplay_sport_menu.click_item(football_tab)

        try:
            self.__class__.event = self.get_event_from_league(event_name=self.live_event_name,
                                                              event_id=self.eventID,
                                                              section_name=self.section_name)
        except VoltronException:
            sleep(5)
            self.device.refresh_page()
            self.__class__.event = self.get_event_from_league(event_name=self.live_event_name,
                                                              event_id=self.eventID,
                                                              section_name=self.section_name)

        self.assertTrue(self.event, msg=f'Event: "{self.live_event_name}" not found in: "{self.section_name}"')

    def test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page(self):
        """
        DESCRIPTION: Verify price change for 'Match Betting' market outcome for one of the Live events from the current page
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - pink color if price has increased
        EXPECTED: The whole button changes color on Coral, only digits change color on Ladbrokes
        """
        self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)
        result = wait_for_result(lambda: self.get_price_button(event=self.event).name == self.new_price,
                                 timeout=30,
                                 expected_result=True,
                                 bypass_exceptions=(
                                     NoSuchElementException, StaleElementReferenceException, VoltronException),
                                 name=f'Price to be changed')
        self.assertTrue(result, msg=f'Price was not changed')

    def test_002_verify_suspension_on_event_market_outcome_level_for_one_of_the_events_from_the_current_page(self):
        """
        DESCRIPTION: Verify suspension on event/market/outcome level for one of the events from the current page
        EXPECTED: Corresponding 'Price/Odds' buttons are displayed as greyed out and become disabled
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event',
                                        expected_result=False)

    def test_003_verify_unsuspension_on_event_market_outcome_level_for_one_of_the_events_from_the_current_page(self):
        """
        DESCRIPTION: Verify unsuspension on event/market/outcome level for one of the events from the current page
        EXPECTED: Corresponding 'Price/Odds' buttons are displayed as active and clickable
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event')

    def test_004_repeat_steps_1_3_for_homepage_featured_tab_section(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section **Mobile**
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            module = self.wait_for_featured_module(name=self.module_title, raise_exceptions=False)
            self.softAssert(self.assertIsNotNone, module,
                            msg=f'Section "{self.module_title}" is not found among FEATURED_STRUCTURE_CHANGE')

            home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            featured_module = self.site.home.get_module_content(home_featured_tab_name)
            featured_module.scroll_to()

            self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_title)
            self.assertTrue(self.section, msg=f'Section "{self.module_title}" is not found on FEATURED tab')

            self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()
            self.test_002_verify_suspension_on_eventmarketoutcome_level_for_one_of_the_events_from_the_current_page()
            self.test_003_verify_unsuspension_on_eventmarketoutcome_level_for_one_of_the_events_from_the_current_page()

    def test_005_repeat_steps_1_3_for_homepage_in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Homepage -> 'In-Play' tab
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state(state_name='Homepage')

            league_name = self.section_name.title() if self.brand != 'ladbrokes' and self.device_type == 'mobile' else self.section_name
            self.__class__.event = self.get_event_for_homepage_inplay_tab(sport_name=self.sport_name,
                                                                          league_name=league_name,
                                                                          event_name=self.live_event_name)
            self.assertTrue(self.event, msg=f'Event: "{self.live_event_name}" not found in: "{self.section_name}"')

            self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            expected_result=False,
                                            section_name=self.section_name,
                                            level='event')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            section_name=self.section_name,
                                            level='event')

    def test_006_repeat_steps_1_3_for_homepage_in_play_module_mobile(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            resp = get_in_play_module_from_ws()
            self.softAssert(self.assertTrue, resp, msg='Inplay module is not configured for Homepage Featured tab')

            sports_name = [sport_segment.get('categoryName') for sport_segment in resp['data']]
            sport_number = sports_name.index(self.sport_name.title())

            self.__class__.sport_number = sport_number + 1
            self.__class__.in_play_event_count = self.cms_config.get_inplay_event_count()
            self.__class__.sport_event_count = self.cms_config.get_sport_event_count(
                sport_number=self.sport_number)
            initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
                sport_category=self.ob_config.backend.ti.football.category_id)
            sport_event_count = initial_number_of_events + 30
            inplay_event_count = initial_number_of_events + 90

            self.cms_config.update_inplay_event_count(event_count=inplay_event_count)
            self.cms_config.update_inplay_sport_event_count(sport_number=self.sport_number,
                                                            event_count=sport_event_count)
            sleep(10)  # to avoid delays in CMS
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage', timeout=15)

            sections = self.site.home.tab_content.in_play_module.items_as_ordered_dict
            ui_sport_name = self.sport_name.title() if not self.brand == 'ladbrokes' else self.sport_name

            section = sections.get(ui_sport_name)
            self.assertTrue(section, msg=f'"{ui_sport_name}" league not found')

            events = section.items_as_ordered_dict
            self.assertTrue(events, msg='There is no Events on the page')

            self.__class__.event = events.get(self.live_event_name)
            self.softAssert(self.assertTrue, self.event,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')

            self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
            self.check_event_odds_state(event=self.event, expected_result=False, level='event')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
            self.check_event_odds_state(event=self.event, level='event')

    def test_007_repeat_steps_1_3_in_play_page_watch_live_tab(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state('in-play')

        events = self.get_inplay_events(sport_name=self.sport_name,
                                        league_name=self.league_name_in_play_live_watch_live,
                                        watch_live_page=True)
        self.assertTrue(events, msg='There is no Events on the page')

        self.__class__.event = events.get(self.live_event_name)
        self.softAssert(self.assertTrue, self.event,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')

        self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.check_event_odds_state(event=self.event, expected_result=False, level='event')

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.check_event_odds_state(event=self.event, level='event')

    def test_008_repeat_steps_1_3_for_sports_landing_page_in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')

        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        self.site.wait_content_state('Football')

        events = self.get_inplay_events(league_name=self.section_name, watch_live_page=False)
        self.assertTrue(events, msg='There is no Events on the page')

        self.__class__.event = events.get(self.live_event_name)
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')

        self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        expected_result=False,
                                        section_name=self.section_name,
                                        level='event')

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.verify_price_buttons_state(event_id=self.eventID,
                                        section_name=self.section_name,
                                        level='event')

    def test_009_repeat_steps_1_3_for_sports_landing_page_in_play_module_mobile_in_play_live_stream_section_on_homepage_desktop_sports_landing_page_matches_tab_in_play_widget_desktop_sports_landing_page_matches_tab_live_stream_widget_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')
            self.site.football.tabs_menu.click_button(self.expected_sport_tabs.in_play)
            self.site.wait_content_state('Football')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)
            league_sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(league_sections, msg='In-Play module has no any sections')

            self.__class__.section = league_sections.get(self.ui_section_name)
            self.assertTrue(self.section, msg=f'"{self.ui_section_name}" not found in leagues: "{league_sections.keys()}"')

            events = self.section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No event found in "{self.ui_section_name}"')

            self.__class__.event = events.get(self.live_event_name)
            self.softAssert(self.assertTrue, self.event,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')

            self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
            self.check_event_odds_state(event=self.event, expected_result=False, level='event')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
            self.check_event_odds_state(event=self.event, level='event')

    def test_010_repeat_steps_1_3_for_in_play_live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            in_play_tabs = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu
            in_play_tabs.click_button(vec.sb.LIVE_STREAM.upper())
            self.assertEqual(in_play_tabs.current, vec.sb.LIVE_STREAM.upper(),
                             msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected. Actual "{in_play_tabs.current}"')

            leagues = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            events = self.section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found in "{self.league_name_in_play_live_stream_homepage}" section')
            self.__class__.event = events.get(self.live_event_name)
            self.softAssert(self.assertTrue, self.event,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')

            self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            expected_result=False,
                                            section_name=self.section_name,
                                            level='event')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            section_name=self.section_name,
                                            level='event')

    def test_011_repeat_steps_1_3_for_in_play_live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='Home')
            self.site.wait_content_state('Homepage')
            self.site.home.tabs_menu.click_button(vec.sb.LIVE_STREAM.upper())
            self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(vec.sb.LIVE_STREAM.upper()).is_selected(),
                            msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected')
            leagues = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.live_section_name)
            self.assertTrue(self.section, msg=f'"{self.live_section_name}" league not found')

            self.__class__.event = self.section.get(self.live_event_name)
            self.softAssert(self.assertTrue, self.event,
                            msg=f'Event {self.live_event_name} was not found in the list of events {self.section.keys()}')

            self.test_001_verify_price_change_for_match_betting_market_outcome_for_one_of_the_live_events_from_the_current_page()

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            expected_result=False,
                                            section_name=self.section_name,
                                            level='event')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            section_name=self.section_name,
                                            level='event')

    def test_011_repeat_steps_1_3_for_sports_landing_page_matches_tab_in_play_widget_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Sports Landing page -> 'Matches' tab -> 'In-Play' widget **Desktop**
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')

            in_play_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                       self.ob_config.football_config.category_id)
            self.site.football.tabs_menu.click_button(in_play_tab_name)

            sections = self.site.football.in_play_widget.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Football page')

            section = sections.get(self.widget_section_name)
            self.assertTrue(section, msg=f'Can not get "{self.widget_section_name}"in {sections.keys()}')

            events = section.content.items_as_ordered_dict
            self.assertTrue(events, msg='No events found')

            event = events.get(self.live_event_name)
            self.softAssert(self.assertTrue, event,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')

            price_buttons = event.odds_buttons.items_as_ordered_dict
            self.assertTrue(price_buttons, msg='Price buttons were not found')

            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=self.new_price)
            price = list(price_buttons.values())[0]
            result = wait_for_result(lambda: price.name == self.new_price,
                                     timeout=30,
                                     expected_result=True,
                                     bypass_exceptions=(
                                         NoSuchElementException, StaleElementReferenceException, VoltronException),
                                     name=f'Price to be changed')
            self.softAssert(self.assertTrue, result,
                            msg=f'Price was not changed. Actual "{price.name}" != Expected "{self.new_price}"')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

            disable_price_buttons = event.odds_buttons.items_as_ordered_dict
            self.assertTrue(disable_price_buttons, msg='Price buttons were not found')

            for button_name, button in disable_price_buttons.items():
                result = button.is_enabled(timeout=6, expected_result=False)
                self.assertFalse(result, msg=f'Price button "{button_name}" was not disabled')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

            enable_price_buttons = event.odds_buttons.items_as_ordered_dict
            self.assertTrue(price_buttons, msg='Price buttons were not found')

            for button_name, button in enable_price_buttons.items():
                result = button.is_enabled(timeout=6)
                self.assertTrue(result, msg=f'Price button "{button_name}" was disabled after another selection suspended')

    def test_012_repeat_steps_1_3_for_sports_landing_page_matches_tab_live_stream_widget_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Sports Landing page -> 'Matches' tab -> 'Live Stream' widget **Desktop**
        """
        if self.device_type == 'desktop':
            widgets = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle')
            if not widgets:
                widgets = self.cms_config.get_system_configuration_item('DesktopWidgetsToggle')
            widget_available = widgets.get('liveStream')
            self.softAssert(self.assertTrue, widget_available, msg='"Live Stream" widget is not configured in CMS')

            self.site.login()
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')

            event = self.site.football.live_stream_widget
            self.softAssert(self.assertTrue, self.live_event_name in event.name,
                            msg=f'Event "{self.live_event_name}" was not found')

            price_buttons = event.items_as_ordered_dict
            self.assertTrue(price_buttons, msg='Price buttons were not found')

            new_widget_price_value = '2/5'
            self.ob_config.change_price(selection_id=self.live_now_selection_id, price=new_widget_price_value)
            price = list(price_buttons.values())[0]
            result = wait_for_result(lambda: price.outcome_price_text == new_widget_price_value,
                                     timeout=30,
                                     expected_result=True,
                                     bypass_exceptions=(
                                         NoSuchElementException, StaleElementReferenceException, VoltronException),
                                     name=f'Price to be changed')

            self.assertTrue(result, msg=f'Price was not changed. Actual "{price.outcome_price_text}" != Expected "{new_widget_price_value}"')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            expected_result=False,
                                            section_name=self.section_name,
                                            level='event')

            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
            self.verify_price_buttons_state(event_id=self.eventID,
                                            section_name=self.section_name,
                                            level='event')
