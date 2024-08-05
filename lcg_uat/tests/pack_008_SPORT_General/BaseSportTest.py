import json
import re
from collections import namedtuple
from collections import OrderedDict
from time import sleep

from crlat_cms_client.utils.exceptions import CMSException
from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import simple_filter
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

import tests
import voltron.environments.constants as vec
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.failure_exception import TestFailure
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.stats_centre_client.stats_centre import StatsCentre
from voltron.utils.waiters import wait_for_result


class BaseSportTest(Common):
    sport_name = None
    expected_sport_tab_keys = namedtuple('expected_sport_tab_keys',
                                         ['in_play', 'matches', 'competitions', 'coupons', 'outrights', 'accumulators', 'accas',
                                          'jackpot', 'specials', 'player_bets', 'results', 'private_market', 'events'])
    expected_sport_tabs = expected_sport_tab_keys(in_play='IN-PLAY', matches='MATCHES', competitions='COMPETITIONS',
                                                  coupons='COUPONS', outrights='OUTRIGHTS', accumulators='ACCUMULATORS', accas='ACCAS',
                                                  jackpot='JACKPOT', specials='SPECIALS', player_bets='PLAYER BETS',
                                                  results='RESULTS', private_market='YOUR ENHANCED MARKETS', events='EVENTS')
    expected_sport_tab_names = expected_sport_tabs._asdict().values()

    date_tabs_keys = namedtuple('date_tabs', ['today', 'tomorrow', 'future'])
    date_tabs = date_tabs_keys(today='TODAY', tomorrow='TOMORROW', future='FUTURE')

    expanded_count = 0
    expected_fixture_header_1 = None
    expected_fixture_header_2 = None
    expected_fixture_header_3 = None
    ew_terms = {'ew_places': 2, 'ew_fac_num': 1, 'ew_fac_den': 16}
    name_of_day_today_short = get_date_time_as_string(time_format="%a")
    name_of_day_tomorrow_short = get_date_time_as_string(time_format="%a", days=1)
    future_date_short = get_date_time_as_string(time_format="%d %b", days=2)
    event_name = None
    event_names = []
    event_name_on_sports_page = None
    eventIDs_names = OrderedDict()
    eventIDs_outcomes = OrderedDict()
    all_prices = OrderedDict()
    jackpot_query = query_builder() \
        .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, 'V15')) \
        .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE))

    def get_fixture_headers_from_cms(self, sport_name):
        try:
            template_type = self.cms_config.get_fixture_header(sport_name=sport_name)
        except CMSException as e:
            self._logger.warning(f'*** Could not find "{sport_name}" sport in Olympic Sports list in CMS. '
                                 f'Using default "1/2/3" headers. Original CMS error: {e}')
            template_type = 'oneTwoType'
        if template_type == 'homeDrawAwayType':
            self.__class__.expected_fixture_header_1 = vec.sb.HOME
            self.__class__.expected_fixture_header_2 = vec.sb.DRAW
            self.__class__.expected_fixture_header_3 = vec.sb.AWAY
        elif template_type == 'oneTwoType':
            self.__class__.expected_fixture_header_1 = '1'
            self.__class__.expected_fixture_header_2 = '2'
            self.__class__.expected_fixture_header_3 = '3'

    def verify_section_fixture_header(self, section):
        section_name = section.name
        if section_name not in self.section_skip_list and section.has_fixture_header():
            fixture_header = section.fixture_header
            fixture_header.scroll_to()
            fixture_header_1 = fixture_header.header1
            fixture_header_2 = fixture_header.header2
            fixture_header_3 = fixture_header.header3
            items_qty = len(fixture_header.items_as_ordered_dict)
            if items_qty == 2:
                self.__class__.expected_fixture_header_2 = None
            self._logger.debug('*** Odds header: first header text: "%s", second: "%s", third: "%s" for section "%s"'
                               % (fixture_header_1, fixture_header_2, fixture_header_3, section_name))
            self.assertTrue(fixture_header_1 == self.expected_fixture_header_1,
                            msg='First odds header text "%s" is not the same as expected text "%s" for section "%s"'
                                % (fixture_header_1, self.expected_fixture_header_1, section_name))
            self.assertTrue(fixture_header_2 == self.expected_fixture_header_2,
                            msg='Third odds header text "%s" is not the same as expected text "%s" for section "%s"'
                                % (fixture_header_2, self.expected_fixture_header_2, section_name))
            if fixture_header_2 is not None or fixture_header_2 != '':
                self.assertTrue(fixture_header_2 == self.expected_fixture_header_2,
                                msg='Second odds header text "%s" is not the same as expected text "%s" for section "%s"'
                                    % (fixture_header_2, self.expected_fixture_header_2, section_name))
        else:
            self._logger.warning('*** Skipping section odds header check as section name "%s" is found in section skip list' % section_name)

    def get_scoreboard_sport_status(self, sport_id) -> bool:
        """
        Method to get 'ScoreboardsSports' parameter for sport
        :param sport_id: int for example for football=16, tennis=34
        :return: bool
        """
        scoreboard_sport_config = self.get_initial_data_system_configuration().get('ScoreboardsSports', {})
        if not scoreboard_sport_config:
            scoreboard_sport_config = self.cms_config.get_system_configuration_item('ScoreboardsSports')
        scoreboard_status = scoreboard_sport_config.get(str(sport_id))
        return scoreboard_status

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type(StaleElementReferenceException), reraise=True)
    def get_event_for_homepage_inplay_tab(self,
                                          sport_name: str,
                                          league_name: str,
                                          event_name: str,
                                          inplay_section: str = vec.inplay.LIVE_NOW_EVENTS_SECTION,
                                          raise_exceptions: bool = True):
        """
        Separate method to get event on Homepage -> In-Play tab
        :param sport_name: Name of sport (e.g. FOOTBALL, HANDBALL)
        :param league_name: Name of league (OB type) (e.g. Championship, Salisbury)
        :param event_name: Event name
        :param raise_exceptions:
        :return: Event object from Homepage -> In-Play tab
        """
        modules = self.cms_config.get_initial_data().get('modularContent', [])
        modules_name = [module.get('id') for module in modules]
        self.softAssert(self.assertIn, self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play, modules_name,
                        msg=f'In-play tab isn\'t shown on Homepage')
        tab_content = self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play))
        inplay_sections = (vec.inplay.LIVE_NOW_SWITCHER.upper(), vec.inplay.UPCOMING_SWITCHER)
        if inplay_section.upper() not in inplay_sections:
            raise VoltronException(f'In-Play Section "{inplay_section}" is not allowed. Possible sections: {inplay_sections}')
        inplay_section_ = tab_content.live_now if inplay_section.upper() == vec.inplay.LIVE_NOW_SWITCHER.upper() else tab_content.upcoming
        sport_sections = inplay_section_.items_as_ordered_dict
        self.assertTrue(sport_sections, msg=f'No one sport section found in "{inplay_section}"')
        sport_section = sport_sections.get(sport_name)

        self.assertTrue(sport_section, msg=f'Sport "{sport_name}" is not found in {list(sport_sections.keys())}')
        sport_section.expand()
        league_sections = sport_section.items_as_ordered_dict
        self.assertTrue(league_sections, msg=f'No Leagues for "{sport_name}" found')
        league = league_sections.get(league_name)
        if not league and sport_section.has_show_more_leagues_button():
            sport_section.show_more_leagues_button.click()
            wait_for_result(lambda: sport_section.has_show_more_leagues_button(expected_result=False, timeout=0),
                            name='No show all button',
                            expected_result=False,
                            timeout=5)
            league_sections = sport_section.items_as_ordered_dict
            self.assertTrue(league_sections, msg=f'No Leagues for "{sport_name}" found')
            league = league_sections.get(league_name)

        self.assertTrue(league, msg=f'League "{league_name}" not found in {list(league_sections.keys())}')
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found for "{league_name}"')
        event = events.get(event_name)
        if raise_exceptions:
            self.assertTrue(event, msg=f'Event "{event_name}" not found')
        return event

    def get_inplay_accordion(self, name, refresh=True):
        def get_accordions():
            if self.device_type == 'mobile':
                accordions_ = self.site.inplay.tab_content.live_now.items_as_ordered_dict
            else:
                accordions_ = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            return accordions_
        accordions = get_accordions()
        self.assertTrue(accordions, msg=f'No sports sections found for "{name}" sport')
        if refresh and not accordions.get(name):
            sleep(3.5)  # TODO VOL-5474
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='in-play')
            accordions = get_accordions()
        return accordions.get(name)

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def get_inplay_events(self, sport_name=None, league_name=None, watch_live_page=True):
        if watch_live_page:
            section = self.get_inplay_accordion(name=sport_name)
            self.assertTrue(section, msg=f'"{sport_name}" section not found')
            section.expand()
            if section.has_show_more_leagues_button():
                section.show_more_leagues_button.click()
            leagues = section.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found in "{sport_name}" section')
            league = leagues.get(league_name)
            self.assertTrue(league, msg=f'"{league_name}" league not found among leagues "{leagues.keys()}"')
            league.expand()
            events = league.items_as_ordered_dict
        else:
            section = self.get_inplay_accordion(name=league_name)
            self.assertTrue(section, msg=f'"{league_name}" section not found')
            section.expand()
            events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events were found for "{league_name}" league')
        return events

    def verify_event_time_is_present(self, event):
        event_time = event.event_time
        event_is_live = event.is_live_now_event
        event_is_half_time = event.is_half_time_event()
        event_has_set_number = event.has_set_number()  # for tennis
        self._logger.debug('*** Event time: {0}'.format(event_time))
        self.assertTrue(any([event_time != '', event_is_live, event_has_set_number, event_is_half_time]),
                        msg='Event time string is empty for event "%s"' % event.event_name)

    def is_event_present(self, section_name, event_name, is_present=True, timeout=5):
        """
        Verifies if event is displayed within the section. Used only on Homepage
        :param section_name: specifies the name of the section to look into
        :param event_name: specifies the name of event to look for
        :param is_present: specifies expected result (if event is displayed or not)
        :param timeout:
        :return: True if event is displayed in the section, False otherwise
        """
        self.site.wait_content_state('Homepage')
        # added this check as currently this method works only on homepage
        self._logger.debug('*** Event name: %s' % event_name)
        module_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

        def _is_event_present():
            sections = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            if not sections:
                return False
            if section_name not in sections.keys():
                return False
            section = sections[section_name]
            section.expand()
            events = section.items_as_ordered_dict
            if not events:
                return False
            return event_name in events.keys()

        result = wait_for_result(lambda: _is_event_present(),
                                 expected_result=is_present,
                                 timeout=timeout,
                                 bypass_exceptions=(NoSuchElementException,
                                                    StaleElementReferenceException,
                                                    KeyError),
                                 name=f'Event "{event_name}" displaying state mach "{is_present}" in section "{section_name}"')
        return result

    def _verify_event_name(self, event):
        event_name = event.event_name
        self.assertTrue(event_name, msg='Event name is empty')
        self._logger.debug(f'*** Event name: {event_name}')
        result = re.match(tests.settings.section_event_market_name_pattern, event_name, re.UNICODE)
        self.assertTrue(result,
                        msg=f'Event name "{event_name}" not matching pattern "{tests.settings.section_event_market_name_pattern}"')

    def verify_section_header_titles(self, outrights=False):
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No events present on page')
        for section_name, section in list(sections.items())[:self.max_number_of_sections]:
            self._logger.debug('*** Section name: %s' % section_name)
            result = re.match(tests.settings.section_event_market_name_pattern, section_name.split('\n')[0], re.U)
            self.assertTrue(result, msg='Item text "%s" not matching pattern "%s"'
                                        % (section_name.split('\n')[0], tests.settings.section_event_market_name_pattern))
            if not outrights:
                section.expand()
                try:
                    self.assertTrue(section.is_expanded(), msg='Cannot expand the section %s' % section.name)
                except StaleElementReferenceException:
                    section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
                    if not section:
                        continue
                    self.assertTrue(section.is_expanded(), msg='Cannot expand the section %s' % section.name)
                self.verify_section_fixture_header(section)
            else:
                pass

    def verify_cashout_label(self, is_available=True):
        is_displayed = None
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        if sections:
            for section_name, section in sections.items():
                self._logger.debug('*** Section name: "%s"' % section_name)
                result = re.match(tests.settings.section_event_market_name_pattern, section_name, re.U)
                self.assertTrue(result, msg='Section name: "%s" not matching pattern "%s"'
                                            % (section_name, tests.settings.section_event_market_name_pattern))
                section_with_cashout = section.group_header.has_cash_out_mark()
                if not is_available:
                    is_displayed = False
                    self.assertFalse(section_with_cashout, msg='Section "%s" contains "CashOut" icon' % section_name)
                elif section_with_cashout:
                    is_displayed = True
                self._logger.debug('*** Cashout available: "%s" for section: "%s"' % (section_with_cashout, section_name))
            if is_available and not is_displayed:
                raise TestFailure('No one section does not contains "CashOut" icon')
        else:
            self._logger.warning('*** No event sections are present on page ')

    def verify_event_section(self, us_sports=False):
        if '/in-play' in self.device.get_current_url():
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one event section found')
        else:
            sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event sections are present on page')
        for section_name, section in list(sections.items())[:self.max_number_of_sections]:
            section.expand()
           # section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
            self._logger.info('*** Section name: %s' % section_name)
            section_items = section.items_as_ordered_dict
            self.assertTrue(section_items, msg='No events found in event section: "%s"' % section_name)
            for event_name, event in list(section_items.items())[:self.max_number_of_events]:
                self.verify_event_time_is_present(event) if section_name != 'ENHANCED MULTIPLES' else \
                    self._logger.warning('*** Skipping verification as there is no such property as event time for ENHANCED MULTIPLES')
                self._verify_event_name(event)
                all_prices = event.get_active_prices()
                self._logger.debug(f'*** Event price/odds buttons: [{all_prices.keys()}]') if all_prices else \
                    self._logger.warning('*** Event does not have active selections')
                has_markets = event.has_markets()
                if has_markets:
                    markets = event.get_markets_count_string()
                    self.softAssert(self.assertRegexpMatches, markets, tests.settings.market_link_pattern,
                                    msg='Item text "%s" not matching pattern "%s"'
                                        % (markets, tests.settings.market_link_pattern))

    def verify_section_collapse_expand(self):
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on page')
        # work-around for Competitions page: A-Z sections is the last section on page, however the rest of sections are sorted alphabetically
        az_section_name, az_section = sections.popitem('A-Z') if 'A-Z' in sections.keys() else (None, None)
        if not self.expanded_count:
            if 'ENHANCED MULTIPLES' in sections:
                self.__class__.expanded_count = 4
            else:
                self.__class__.expanded_count = 3
        if az_section and az_section_name:
            list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.items())[self.expanded_count:self.max_number_of_sections].append((az_section_name, az_section))

        for section_name, section in list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.items())[:self.expanded_count]:
            self._logger.debug('*** Section %s' % section_name)
            self.assertTrue(section.is_expanded(),
                            msg='The section %s are not expanded by default' % section_name)
            try:
                section.scroll_to()
                section.collapse()
                section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
                if not section:
                    raise StaleElementReferenceException(f'Section "{section_name}" not found, assuming page content got refreshed')
                self.assertFalse(section.is_expanded(expected_result=False, timeout=1),
                                 msg=f'Cannot collapse the section "{section_name}"')
                section.expand()
            except StaleElementReferenceException:
                self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
                actual_section_name=section_name.split('\n')[0]
                section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(actual_section_name)
                self.assertTrue(section, msg=f'"{actual_section_name}" not found')
                section.scroll_to()
                section.collapse()
                section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
                if not section:
                    continue
                self.assertFalse(section.is_expanded(expected_result=False, timeout=1),
                                 msg=f'Cannot collapse the section "{section_name}"')
                section.expand()

        for section_name, section in list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.items())[self.expanded_count:self.max_number_of_sections]:
            self._logger.debug('*** Section %s' % section_name)
            self.assertFalse(section.is_expanded(expected_result=False, timeout=1),
                             msg=f'The remaining section "{section_name}" is not collapsed by default')
            try:
                section.scroll_to()
                section.expand()
                section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
                if not section:
                    raise StaleElementReferenceException(
                        f'Section "{section_name}" not found, assuming page content got refreshed')
                self.assertTrue(section.is_expanded(timeout=1), msg=f'Cannot expand the section "{section_name}"')
            except StaleElementReferenceException:
                section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
                if not section:
                    continue
                self.assertTrue(section.is_expanded(), msg=f'Cannot expand the section "{section_name}"')

            section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
            section.collapse()

    def verify_future_event_start_time(self):
        sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No events present on page')
        for section_name, section in list(sections.items())[:self.max_number_of_sections]:
            if section_name not in self.section_skip_list:
                for event in list(section.items_as_ordered_dict.values())[:self.max_number_of_events]:
                    event_day = event.event_date
                    self.assertNotEqual(event_day, self.name_of_day_today_short,
                                        msg='Today events are shown on future tab')
                    self.assertNotEqual(event_day, self.name_of_day_tomorrow_short,
                                        msg='Tomorrows\'s events are shown on future tab')

    def verify_sorting_type_buttons(self, expected_sorting_types_buttons=None,
                                    expected_active_btn=vec.inplay.LIVE_NOW_SWITCHER):
        """
        Verifies that sorting types buttons match expected and active one is expected as well.
        :param expected_sorting_types_buttons: Specifies list of expected buttons names
        :param expected_active_btn: Specifies the name of the button which is expected to be active
        """
        if expected_sorting_types_buttons is None:
            expected_sorting_types_buttons = [vec.inplay.LIVE_NOW_SWITCHER,
                                              vec.inplay.UPCOMING_SWITCHER]
        sorting_types_btns = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
        active_btn = self.site.inplay.tab_content.grouping_buttons.current
        self.assertEqual(len(sorting_types_btns), len(expected_sorting_types_buttons),
                         msg='The number of sorting type buttons does not match, "%s" != "%s"'
                             % (len(sorting_types_btns), len(expected_sorting_types_buttons)))
        self.assertListEqual(list(sorting_types_btns.keys()), expected_sorting_types_buttons,
                             msg='Current sorting types buttons: %s does not match with expected: %s'
                                 % (list(sorting_types_btns.keys()), expected_sorting_types_buttons))
        self.assertEqual(active_btn, expected_active_btn,
                         msg=f'"{expected_active_btn}" sorting type is not selected by default')

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type((StaleElementReferenceException, AttributeError)),
           reraise=True)
    def verify_active_sport_on_inplay_page(self, sport_name: str = None) -> None:
        """
        Verifies active sport on in play page, if sport parameter is not specified - verifies if the default sport
        (first one) is selected and highlighted
        :param sport_name: Sport name like it is configured in CMS: FOOTBALL, BASEBALL
        :return: None
        """
        try:
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        except (StaleElementReferenceException, VoltronException):
            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports, msg='List of sports buttons was not found')
        if sport_name:
            try:
                self.site.inplay.inplay_sport_menu.wait_item_appears(item_name=sport_name)
            except (StaleElementReferenceException, VoltronException):
                self.site.inplay.inplay_sport_menu.wait_item_appears(item_name=sport_name)
            self.assertTrue(sport_name in sports.keys(), msg=f'"{sport_name}" not found in "{sports.keys()}"')
            self.assertTrue(self.site.inplay.inplay_sport_menu.items_as_ordered_dict.get(sport_name).is_selected(),
                            msg=f'"{sport_name}" is not selected')
        else:
            # Icon at index 0 is WATCH LIVE, so picking icon with index 1
            default_sport_name = list(sports.keys())[1]

            # Getting item again in order to not receive StaleElementException
            is_selected = self.site.inplay.inplay_sport_menu.items_as_ordered_dict.get(default_sport_name).is_selected()
            self.assertTrue(is_selected, msg=f'"{default_sport_name}" is not selected by default')

    def verify_event_on_favourites_page(self, expected_events=None):
        """
        :param expected_events: list or tuple with expected event names
        """
        sections = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Sections are not found')
        section = list(sections.values())[0]
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='Events are not found')

        # if one event is added to favourites
        if not expected_events:
            expected_events = tuple((self.event_name,))
        self._logger.info('*** Found events: %s' % events.keys())
        self.assertEqual(len(events), len(expected_events),
                         msg='Found %d events %s while expected %d %s'
                             % (len(events), events.keys(), len(expected_events), expected_events))
        for event in expected_events:
            self.assertTrue(event in events.keys(), msg='Event %s is not found' % event)

    def verify_tabs_length(self):
        items = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertTrue(len(items) >= 4,
                        msg='Number of tabs is not in expected range: expected 4 or more, found "%s"'
                            % len(items))

    def verify_default_tabs(self):
        items = self.site.contents.tabs_menu.items_as_ordered_dict
        self.assertTrue(len(set(items.keys()).intersection(self.expected_sport_tab_names)) >= 4,
                        msg='There are few expected tab missed: %s, current tabs list is: %s'
                            % (self.expected_sport_tab_names, items.keys()))

    def verify_default_tabs_with_cms(self, category_id: int):
        """
        :param category_id: sport ID hardcoded in backend_config.yaml
        """
        tabs_in_cms = self.get_visible_sport_tabs(category_id=category_id)
        initial_expected_tabs = [tab.get('label').upper() for tab in tabs_in_cms]
        expected_tabs = initial_expected_tabs if self.device_type != 'desktop' else ['IN-PLAY'] + initial_expected_tabs
        actual_tabs = self.site.contents.tabs_menu.items_as_ordered_dict

        self.assertEqual(
            set(actual_tabs.keys()).intersection(expected_tabs),
            actual_tabs.keys(),
            msg=f'There are few expected tabs missed: Expected: \n"{expected_tabs}". '
                f'Current tabs list: \n"{list(actual_tabs.keys())}"')

    def verify_edp_market_tabs_order(self, edp_market_tabs):
        """
        :param edp_market_tabs: list of market tabs from EDP page
        :return:
        """
        cms_market_tabs = self.cms_config.get_market_tabs_order()
        self.assertTrue(cms_market_tabs, msg='EDP market tabs list from CMS is empty')
        cms_market_tabs = [market.upper() for market in cms_market_tabs]

        cms_markets_order = [(market, cms_market_tabs.index(market)) for market in cms_market_tabs]
        cms_markets_order.sort(key=lambda x: x[1])
        cms_markets_order_as_dict = OrderedDict(cms_markets_order)
        cms_markets_order_list = cms_markets_order_as_dict.keys()

        expected_edp_market_tabs = [market for market in edp_market_tabs if market in set(cms_markets_order_list)]
        expected_cms_market_tabs = [market for market in cms_markets_order_list if market in set(edp_market_tabs)]

        self._logger.debug('*** EDP markets tabs: "%s",\n CMS markets tabs "%s"'
                           % (expected_edp_market_tabs, expected_cms_market_tabs))
        self.assertListEqual(expected_edp_market_tabs, expected_cms_market_tabs,
                             msg='List of tabs on EDP "%s" is not the same as from CMS "%s"'
                                 % (expected_edp_market_tabs, expected_cms_market_tabs))

    def verify_prices_not_suspended(self, initial_output_prices):
        for key, value in initial_output_prices.items():
            self.assertFalse(initial_output_prices[key] == 'S', 'Initial Price is suspended for "{0}"'.format(key))

    def verify_prices(self, actual_prices, expected_prices):
        self._logger.debug('*** Expected prices %s' % expected_prices)
        self._logger.debug('*** Actual prices %s' % actual_prices)
        for actual_price, expected_price in zip(actual_prices.values(), expected_prices.values()):
            self.assertEqual(actual_price, expected_price,
                             msg='Incorrect price value. Actual "{0}" is not expected "{1}"'
                             .format(actual_price, expected_price))

    def wait_for_counter_change(self, initial_counters, timeout=5):
        for sport, counter in initial_counters.items():
            wait_for_result(lambda: self.site.inplay.inplay_sport_menu.items_as_ordered_dict[sport].counter > initial_counters[sport],
                            timeout=timeout,
                            bypass_exceptions=(NoSuchElementException,
                                               StaleElementReferenceException,
                                               VoltronException),
                            name=f'Counter was not increased for "{sport}"')

    def verify_last_football_tab(self, tab):
        result = wait_for_result(lambda: self.site.football.tabs_menu.current == tab,
                                 name=f'Tab "{tab}" became active',
                                 timeout=2)
        self.assertTrue(result, msg=f'"{tab}" tab is not active')
        no_events = self.site.football.tab_content.has_no_events_label()
        if no_events:
            pass
        else:
            if 'competitions' == tab.lower() and self.device_type != 'desktop':
                events = self.site.football.tab_content.all_competitions_categories.n_items_as_ordered_dict()
            else:
                events = self.site.football.tab_content.accordions_list
            self.assertTrue(events, msg=f'No events on "{tab}" tab')

    def get_selection_bet_button(self, market_name, selection_name='Draw'):
        selection_name = selection_name.upper()
        if not market_name:
            market_name = self.expected_market_sections.match_result
        market_name = market_name.upper()
        markets = self.site.sport_event_details.tab_content.accordions_list.get_items(name=market_name)
        markets = OrderedDict((key.upper(), value) for key, value in markets.items())
        section = markets.get(market_name)
        self.site.sport_event_details.scroll_to_top()
        self.assertTrue(section, msg=f'"{market_name}" market not present in markets: {list(markets.keys())}')
        section.expand()
        section.scroll_to()
        section.expand()
        output_prices_list = section.outcomes.items_as_ordered_dict
        output_prices_list = OrderedDict((key.upper(), value) for key, value in output_prices_list.items())
        self.assertTrue(output_prices_list, msg='No output prices found')
        outcome = output_prices_list.get(selection_name)
        self.assertTrue(outcome, msg=f'"{selection_name}" not found in {list(output_prices_list.keys())}')
        return outcome.bet_button

    def verify_price_buttons_state(self, event_id, section_name, level, expected_result=True, inplay_section=None, timeout=30):
        """
        Verifies state of price buttons of Match Betting market
        :param event_id: specifies the id of event to look for
        :param section_name: specifies the name of the section to look into e.g. 'AUTO TEST - AUTOTEST PREMIER LEAGUE'
        :param level: level on which status change was made in Backoffice e.g. 'event', 'market', 'selection'
        :param expected_result: specifies expected result. True if buttons should be enabled, False otherwise
        :param timeout: time to wait for button status change
        :return: True if price buttons' state matches expected value
        """
        event = self.get_event_from_league(section_name=section_name, event_id=event_id, inplay_section=inplay_section)
        price_buttons = list(event.get_all_prices().items())
        self.assertTrue(price_buttons, msg='Price buttons are not displayed')

        if expected_result:
            for button_name, button in price_buttons:
                result = button.is_enabled(timeout=timeout, expected_result=expected_result)
                self.assertTrue(result, msg=f'Price button {button_name} was not enabled')
        else:
            if level == 'event' or level == 'market':
                for button_name, button in price_buttons:
                    result = button.is_enabled(timeout=timeout, expected_result=expected_result)
                    self.assertFalse(result, msg=f'Price button {button_name} was not disabled')
            elif level == 'selection':
                button_name, button = price_buttons[0]
                result = button.is_enabled(timeout=timeout, expected_result=expected_result)
                self.assertFalse(result, msg=f'Price button {button_name} was not disabled')

                for button_name, button in price_buttons[1:]:
                    result = button.is_enabled(timeout=timeout, expected_result=not expected_result)
                    self.assertTrue(result, msg=f'Price button {button_name} was disabled after another selection suspended')
            else:
                raise VoltronException('Please specify correct level: event, market or selection')

    def add_selection_from_event_details_to_quick_bet(self, selection_name='Draw', market_name=None):
        if self.brand == 'ladbrokes':
            selection_name = selection_name.upper()
        bet_button = self.get_selection_bet_button(selection_name=selection_name, market_name=market_name)
        self.device.driver.implicitly_wait(1)
        bet_button.click()
        self.device.driver.implicitly_wait(0)
        # self.assertTrue(bet_button.is_selected(timeout=4), msg='Outcome button is not highlighted in green')  # TODO VOL-3609
        self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet is not shown')

    def check_odds_format(self, odds, expected_odds_format='fraction', raise_exceptions=True):
        delimiter_char = '/' if expected_odds_format == 'fraction' else '.'
        if raise_exceptions:
            self.assertIn(delimiter_char, odds,
                          msg=f'Expected odds format is "{expected_odds_format}" but "{delimiter_char}" was not found in odds value "{odds}"')
        else:
            return delimiter_char in odds

    def verify_my_bets_disappeared(self, event):
        self.navigate_to_edp(event.event_id)
        self.assertFalse(self.site.sport_event_details.has_event_user_tabs_list(expected_result=False),
                         msg=f'"{self.my_bets_tab_name}" tab still present but was not expected to be present')

    def get_competition_with_results_and_standings_tabs(self, category_id: (int, str), raise_exceptions=False):
        """
        :param category_id: Category (sport) ID in TI (ex.: 16 - Football)
        :param raise_exceptions: If True performs verification of found class/type, if False - returns namedtuple
        :return: Class (country) and type (league) names with "Results" and "Standings" tabs on Competition details page,
                 and class and type ids. e.g.:
        {
            'class_name': 'Football Morocco',
            'league_name': 'Moroccan Botola'
            'class_id': '24'
            'type_id': '5544'
        }
        """
        sport_name, league_name = None, None
        class_id, type_id = None, None
        sc = StatsCentre(stats_centre_url=tests.settings.stats_centre_url)
        filters = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))
        class_ids_resp = self.ss_req.ss_class(query_builder=filters)

        competitions_football = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_football:
            competitions_football = self.cms_config.get_system_configuration_item('CompetitionsFootball')
        if not competitions_football:
            raise CmsClientException('CompetitionsFootball is not configured in CMS')
        az_class_ids = competitions_football.get('A-ZClassIDs')
        if not az_class_ids:
            raise CmsClientException('A-ZClassIDs are not configured in CMS')
        season_id = None
        for sport_class in class_ids_resp:
            class_id = sport_class['class']['id']
            if class_id in az_class_ids.split(','):
                filters = self.ss_query_builder.add_filter(
                    simple_filter(LEVELS.TYPE, ATTRIBUTES.HAS_OPEN_EVENT, OPERATORS.IS_TRUE))
                leagues_resp = self.ss_req.ss_class_to_sub_type_for_class(class_id=class_id, query_builder=filters)
                for league in leagues_resp[0]['class']['children']:
                    league_id = league['type']['id']
                    sc_data = sc.get_stats_centre_data(category_id=category_id, class_id=class_id, type_id=league_id)
                    if any(season.get('id') and not season.get('error') for season in sc_data):
                        season_id = next(season for season in reversed(sc_data))['id']
                        sport_name = sport_class['class']['name']
                        class_id = sport_class['class']['id']
                        league_name = league['type']['name']
                        type_id = league['type']['id']
                        break
                else:
                    continue
                break

        if raise_exceptions:
            if not sport_name or not league_name:
                raise SiteServeException('Cannot find competition with present "Results" / "Standings" tabs')

        _competition = namedtuple('competition', ('class_name', 'league_name', 'class_id', 'type_id', 'season_id'))
        competition = _competition(class_name=sport_name,
                                   league_name=league_name,
                                   class_id=class_id,
                                   type_id=type_id,
                                   season_id=season_id)
        self._logger.info(f'*** Found Competition: {json.dumps(competition._asdict(), indent=2)}')
        return competition

    def check_sport_presence_on_inplay(self, sport_name: str):
        """
        To verify that sport is active and shown on In Play tab/module
        """
        all_sport_categories = self.cms_config.get_sport_categories()
        sport_present = False
        for sport in all_sport_categories:
            target = sport['targetUri']
            if target and sport_name in target:
                if sport['disabled']:
                    raise CmsClientException('Sport category is disabled in CMS')
                if not sport['showInPlay']:
                    raise CmsClientException('Inplay tab is disabled on Sport landing page')
                sport_present = True
                break
        if not sport_present:
            raise CmsClientException(f'Sport "{sport_name}" not present is the list CMS sport categories')
