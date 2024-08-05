import collections
import json
import random
import re
import time
import datetime as dt
from collections.abc import KeysView
from collections import OrderedDict
from collections.abc import ValuesView
from datetime import datetime
from datetime import timedelta
from fractions import Fraction
from time import sleep

import pytz
from crlat_ob_client.create_event import CreateSportEvent
from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import debug_filter
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import translation_lang
from dateutil.parser import parse
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tzlocal import get_localzone

import tests
import voltron.environments.constants as vec
from tests.base_test import BaseTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.failure_exception import TestFailure
from voltron.utils.exceptions.general_exception import GeneralException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import do_request
from voltron.utils.helpers import get_live_serve_updates
from voltron.utils.helpers import get_live_updates_for_event_on_featured_ms
from voltron.utils.js_functions import determine_day, format_ss_date_to_ui_date
from voltron.utils.performance_log_parser import parse_web_socket_response_by_id
from voltron.utils.performance_log_parser import parse_web_socket_response_by_url
from voltron.utils.waiters import wait_for_result, wait_for_haul


class Common(BaseTest):
    max_number_of_events = 10
    max_number_of_sections = 10
    max_amount_digits_number = 7
    max_amount_decimal_number = 2
    std_cvv_number = '123'
    short_cvv_number = '1'
    long_cvv_number = '1234'
    low_quick_deposit_amount = '4.99'
    min_quick_deposit_amount = '5'
    deposit_top_bar_keys = collections.namedtuple('deposit_top_bar', ['deposit'])
    deposit_top_bar = deposit_top_bar_keys(deposit='DEPOSIT')
    invalid_input_values = ['Az', r'~!@#$%^&()`_+={}|[]\:";', ' ', '']

    fractional_pattern = r'^\d+\/\d+$'
    decimal_pattern = r'^\d+\.\d+$'
    acca_fractional_pattern = r'^\d+[.]*[\d+]*\/\d+$'
    all_selections = {}
    eventID = None
    marketID = None
    selection_ids = OrderedDict()
    event_off_time = None
    team1, team2 = None, None
    user_balance = None
    created_event_name = None
    expected_page_header = None
    section_skip_list = ['NEXT 4 RACES', 'NEXT FOUR', 'NEXT 4', 'ENHANCED MULTIPLES',
                         'MOBILE EXCLUSIVE', 'PRICE BOMB', 'WINNING DISTANCES']
    featured_module_types = ['EventsModule', 'InplayModule', 'SurfaceBetModule', 'HighlightCarouselModule', 'QuickLinkModule']
    _betslip_content = None
    _betslip_loading = None

    @property
    def expected_market_tabs(self):
        return vec.siteserve.EXPECTED_MARKET_TABS

    @property
    def expected_market_sections(self):
        if self.brand == 'ladbrokes':
            return vec.siteserve.EXPECTED_MARKET_SECTIONS_TITLE
        else:
            return vec.siteserve.EXPECTED_MARKET_SECTIONS

    # Time format patterns
    ob_format_pattern = '%Y-%m-%dT%H:%M:%SZ'
    time_format_pattern = '%H:%M - %d %b'

    @staticmethod
    def map_python_to_js_time_format(py_format):
        """
        Map Python time format to JavaScript time format.

        Args:
            py_format (str): Python time format pattern.

        Returns:
            str: JavaScript compatible time format pattern.

        Raises:
            ValueError: If the Python format pattern is not recognized.
        """
        # Mapping of Python time format to JavaScript time format
        format_mapping = {
            '%Y': 'YYYY',
            '%m': 'MM',
            '%d': 'DD',
            '%H': 'HH',
            '%M': 'MIN',
            '%S': 'SS',
            '%b': 'MON|STR',
            '%a': 'DAY'
        }

        # Replace Python format characters with JavaScript format
        js_format = ''
        i = 0
        while i < len(py_format):
            if py_format[i] == '%' and i + 1 < len(py_format):
                js_format += format_mapping.get(py_format[i:i + 2], py_format[i])
                i += 1  # Skip the next character
            else:
                js_format += py_format[i]
            i += 1

        return js_format

    @property
    def event_card_today_time_format_pattern(self):
        return '%H:%M, Today' if self.brand == 'bma' else '%H:%M Today'

    @property
    def event_card_future_time_format_pattern(self):
        return '%H:%M, %d %b'

    @property
    def my_bets_event_today_time_format_pattern(self):
        return '%H:%M, Today'

    @property
    def my_bets_event_future_time_format_pattern(self):
        return '%H:%M, %d %b'

    @property
    def event_card_coupon_and_competition_future_time_format_pattern(self):
        return '%H:%M, %d %b' if self.brand == 'bma' else '%H:%M %d %b'

    # SiteServe filters
    start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
    start_date_minus = get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S", hours=-3)

    @property
    def end_date(self):
        """
        Mobile view default SiteServe filter on UI includes today + tomorrow events, Desktop - only today events
        :return: end date string
        """
        days = 2 if self.device_type != 'desktop' else 1
        end_date = f'{get_date_time_as_string(days=days)}T00:00:00.000Z'
        return end_date

    def basic_active_events_filter(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, self.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      self.start_date_minus))

    # Siteserve requests
    # --------------------
    def get_class_ids_for_category(self, category_id: (int, str) = 16) -> list:
        """
        Gets class ids for given category (sport, races)
        :param category_id: category id of sport/races
        :return: list of class ids
        """
        filters = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))
        class_ids_resp = self.ss_req.ss_class(query_builder=filters)
        return [class_['class']['id'] for class_ in class_ids_resp if class_.get('class') and class_['class'].get('id')]

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(SiteServeException), reraise=True)
    def get_active_events_for_category(self, expected_template_market=None,
                                       number_of_events=1,
                                       category_id: (int, str) = 16,
                                       raise_exceptions: bool = True, **kwargs) -> list:
        """
        Gets active event for given category (sport, racing, etc.)
        :param expected_template_market: expected template market
        :param number_of_events: number of events to be returned
        :param category_id: category id of sport/races
        :param raise_exceptions: whether to raise exception or not if no events found
        :param kwargs: accepts additional_filters - query_builder filter
        :return: event info
        """
        check_lp_price = True
        if not expected_template_market:
            if category_id == self.ob_config.football_config.category_id:
                expected_template_market = 'Match Betting'
            elif category_id == self.ob_config.tennis_config.category_id:
                expected_template_market = 'Match Betting'
            elif category_id == self.ob_config.horseracing_config.category_id:
                expected_template_market = 'Win or Each Way'
                check_lp_price = False
            elif category_id == self.ob_config.backend.ti.greyhound_racing.category_id:
                expected_template_market = 'Win or Each Way'
                check_lp_price = False

        class_ids = self.get_class_ids_for_category(category_id=category_id)
        ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
        additional_filters = kwargs.get('additional_filters')
        is_in_play_event = OPERATORS.IS_TRUE if kwargs.get('in_play_event') else OPERATORS.IS_FALSE
        events_filter = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, is_in_play_event)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, is_in_play_event)) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.NOT_INTERSECTS, 'MKTFLAG_SP'))
        if expected_template_market:
            events_filter.add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS, f'|{expected_template_market}|')))

        if self.brand == 'ladbrokes' and tests.settings.backend_env == 'prod':
                # to skip events from Performance England class. Cannot find same class for coral.
                events_filter.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS,
                                                       self.ob_config.football_config.perf_england.class_id))
        if self.brand != 'ladbrokes':
            # to skip events from Algerian Cup type that is in use for performance runs
            events_filter.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_ID, OPERATORS.NOT_INTERSECTS, '208'))
            events_filter.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '755'))

        # temporary marked, for now we have correct created events
        if tests.settings.backend_env == 'prod':
            # to skip events from ESOCCER class
            events_filter.add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CLASS_ID, OPERATORS.NOT_INTERSECTS, '3092'))

        if additional_filters:
            if not isinstance(additional_filters, (list, tuple)):
                additional_filters = [additional_filters]
            for filter_ in additional_filters:
                events_filter.add_filter(filter_)

        found_events = []
        resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
        self._logger.info(f'*** Found {len(resp)} event(s) for category {category_id} and classes {class_ids}')
        for event in resp:
            if event.get('event') and event['event'].get('children'):
                markets = event['event']['children']
                for market in markets:
                    if expected_template_market and market['market']['templateMarketName'] != expected_template_market:
                        continue

                    if market['market'].get('children'):
                        if not check_lp_price:
                            found_events.append(event)
                        else:
                            for outcome in market['market']['children']:
                                if outcome['outcome'].get('children'):
                                    for child in outcome['outcome']['children']:
                                        if child.get('price'):
                                            found_events.append(event)
                                        break
                                break

        if not found_events and raise_exceptions:
            raise SiteServeException(f'No active events found for category id "{category_id}"')
        random.shuffle(found_events)
        if kwargs.get('all_available_events'):
            return found_events
        if len(found_events) < number_of_events and raise_exceptions:
            raise SiteServeException(
                f'No enough active events for category id "{category_id}"')
        return found_events[:number_of_events]

    def get_active_event_selections_for_category(self, category_id: (int, str) = 16, **kwargs) -> dict:
        """
        Gets dictionary of selections of active events for given category (sport, racing, etc.)
        :param category_id: category id of sport/races
        :return: selection ids
        """
        if category_id == self.ob_config.football_config.category_id:
            expected_template_market = 'Match Betting'
        elif category_id == self.ob_config.tennis_config.category_id:
            expected_template_market = 'Match Betting'
        elif category_id == self.ob_config.horseracing_config.category_id:
            expected_template_market = 'Win or Each Way'
        elif category_id == self.ob_config.backend.ti.greyhound_racing.category_id:
            expected_template_market = 'Win or Each Way'
        elif category_id == self.ob_config.backend.ti.basketball.category_id:
            expected_template_market = 'Money Line'
        else:
            expected_template_market = 'Match Betting'

        event = random.choice(self.get_active_events_for_category(category_id=category_id,
                                                                  expected_template_market=expected_template_market,
                                                                  **kwargs))

        self._logger.info(f'*** Found event with ID "{event.get("event", {}).get("id")}"')

        outcomes = next((market['market']['children'] for market in event['event']['children'] if
                         market['market']['templateMarketName'] == expected_template_market and market['market'].get('children')), None)
        if not outcomes:
            raise SiteServeException(f'No market that match expected "{expected_template_market}" and has outcomes')

        return {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

    def get_active_event_for_class(self, class_id: (int, str), return_all_events: bool = False,
                                   raise_exceptions: bool = True, **kwargs) -> dict:
        """
        Gets active event for given class (sport, racing, etc.)
        :param class_id: class id of sport/races
        :param return_all_events: return all events or max number of events
        :param raise_exceptions: whether to raise exception or not if no events found
        :param kwargs: accepts additional_filters - query_builder filter
        :return: event info
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_id, brand=self.brand)
        additional_filters = kwargs.get('additional_filters')
        events_filter = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A'))
        if additional_filters:
            if not isinstance(additional_filters, (list, tuple)):
                additional_filters = [additional_filters]
            for filter_ in additional_filters:
                events_filter.add_filter(filter_)

        resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
        events = [event for event in resp if
                  event.get('event') and event['event'] and event['event'].get('children')]
        if not events and raise_exceptions:
            raise SiteServeException(
                f'No active events found for class id "{class_id}"')
        if not return_all_events:
            import random
            event_count = self.max_number_of_events if self.max_number_of_events < len(events) else len(events)
            events = random.sample(events, event_count) if events else None

        return events

    def get_suspended_event_for_class(self, class_id: (int, str), return_all_events: bool = False,
                                      raise_exceptions: bool = True, **kwargs) -> dict:
        """
        Gets suspended event for given class (sport, racing, etc.)
        :param class_id: class id of sport/races
        :param return_all_events: return all events or max number of events
        :param raise_exceptions: whether to raise exception or not if no events found
        :param kwargs: accepts additional_filters - query_builder filter
        :return: event info
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_id, brand=self.brand)
        additional_filters = kwargs.get('additional_filters')
        events_filter = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'S')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'S')) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'S'))
        if additional_filters:
            if not isinstance(additional_filters, (list, tuple)):
                additional_filters = [additional_filters]
            for filter_ in additional_filters:
                events_filter.add_filter(filter_)

        resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
        events = [event for event in resp if
                  event.get('event') and event['event'] and event['event'].get('children')]
        if not events and raise_exceptions:
            raise SiteServeException(
                f'No suspended events found for class id "{class_id}"')
        if not return_all_events:
            import random
            event_count = self.max_number_of_events if self.max_number_of_events < len(events) else len(events)
            events = random.sample(events, event_count) if events else None

        return events

    def get_sport_name_for_event(self, event: dict) -> str:
        """
        Gets league name from event response
        :param event - event response
        :return: sport (category) name
        """
        return event['event']['categoryCode'].replace('_', ' ')

    def get_accordion_name_for_event_from_ss(self, event: dict, **kwargs) -> str:
        """
        Gets league name from event response
        :param event - event response
        :param kwargs: in_play_tab_slp - In Play tab on SLP (Sport Landing Page,
        :param kwargs: in_play_tab_home_page - In Play tab on Homepage
        :param kwargs: live_stream_tab_homepage - Live Stream tab on Homepage
        :param kwargs: in_play_page_sport_tab - In Play page sport tab (e.g.: Football, Cricket, etc.)
        :param kwargs: in_play_page_watch_live - In Play page Watch Live tab
        :param kwargs: in_play_module_slp - In Play Module on SLP
        :param kwargs: in_play_module_homepage - In Play Module on Homepage Featured/Highlights tab
        :return: League name
        """
        in_play_tab_slp = kwargs.get('in_play_tab_slp')
        in_play_tab_home_page = kwargs.get('in_play_tab_home_page')
        live_stream_tab_homepage = kwargs.get('live_stream_tab_homepage')
        in_play_page_watch_live = kwargs.get('in_play_page_watch_live')
        in_play_page_sport_tab = kwargs.get('in_play_page_sport_tab')
        in_play_module_slp = kwargs.get('in_play_module_slp')
        in_play_module_homepage = kwargs.get('in_play_module_homepage')
        competition = kwargs.get('competition_page')
        prematch = not any((in_play_tab_slp, in_play_tab_home_page, live_stream_tab_homepage, in_play_page_sport_tab,
                            in_play_page_watch_live, in_play_module_slp, in_play_module_homepage, competition))
        type_name = event['event']['typeName']
        category_code = event['event']['categoryCode'].title().replace('_', ' ')
        class_name = event['event']['className'].replace(category_code, '', 1).lstrip()
        category_id = int(event['event']['categoryId'])

        # categories ids to skip removing 'categoryCode' from accordion name
        categories_to_skip = [self.ob_config.tennis_config.category_id]

        if prematch:
            if category_id in categories_to_skip:
                class_name = event['event']['className']
                league_name = f'{class_name.lstrip().upper()} - {type_name.upper()}'
            else:
                league_name = f'{class_name.replace(category_code, "").lstrip().upper()} - {type_name.upper()}'
            return league_name
        if competition:
            league_name = type_name.title()
            return league_name

        if self.brand != 'ladbrokes':
            if self.device_type != 'desktop':
                if any((in_play_page_watch_live, in_play_tab_home_page, live_stream_tab_homepage, in_play_module_slp)):
                    league_name = type_name
                elif in_play_tab_slp or in_play_page_sport_tab:
                    league_name = type_name.upper()
                elif in_play_module_homepage:
                    league_name = category_code
                else:
                    league_name = type_name
            else:
                if any((in_play_page_watch_live, in_play_page_sport_tab, in_play_tab_home_page, in_play_tab_slp)):
                    league_name = f'{class_name.lstrip()} - {type_name}'.upper()
                else:
                    league_name = type_name
        else:
            if self.device_type != 'desktop':
                if any((in_play_page_watch_live, in_play_tab_home_page, live_stream_tab_homepage,
                        in_play_module_slp, in_play_page_sport_tab, in_play_tab_slp)):
                    league_name = type_name.upper()
                elif in_play_module_homepage:
                    league_name = category_code.upper()
                else:
                    league_name = type_name.upper()
            else:
                if any((in_play_page_sport_tab, in_play_tab_slp, in_play_tab_home_page)):
                    league_name = f'{class_name.lstrip()} - {type_name}'.upper()
                elif any((in_play_page_watch_live, )):
                    league_name = f'{class_name.lstrip()} - {type_name}'.title()
                else:
                    league_name = type_name

        return league_name.strip()

    def get_accordion_name_for_market_from_ss(self, ss_market_name):
        key = ss_market_name.replace(' ', '_').lower()
        accordion_name = next((getattr(self.expected_market_sections, name) for name in self.expected_market_sections._fields if name == key), '')
        return accordion_name
    # -----------------------

    def navigate_to_page(self, name, test_automation=True, **kwargs):
        """
        :param test_automation: True or False
        :param name: 'str'
        Example: 'deposit'
        :return: https://{tests.HOSTNAME}/deposit
        Example: for sports - 'sport/football'
        :return: https://{tests.HOSTNAME}/sport/football
        Example: for racing - 'horse-racing'
        :return: https://{tests.HOSTNAME}/horse-racing
        """
        url = f'https://{tests.HOSTNAME}/{name}'
        self.device.navigate_to(url=url, testautomation=test_automation)
        self.site.wait_splash_to_hide()
        try:
            self.site.close_all_dialogs(async_close=False, timeout=0.5)
        except Exception as e:
            self._logger.info(e)
        if "FOOTBALL" in url.upper():
            self.site.close_qe_or_fanzone_popup(name=name, **kwargs)

    def navigate_to_promotion(self, promo_key):
        promo = f'promotions/details/{promo_key}'
        self.navigate_to_page(promo)
        self.site.wait_content_state('PromotionDetails')

    def navigate_to_edp(self, event_id, sport_name=None, timeout=30):
        """
        Open created event using event id and direct link: https://<hostname>/event/event_id
        :param event_id: int or str
        :param sport_name: str optional page name for correct content state handling
        :param timeout: int
        :return: None
        """
        event_url = f'{tests.HOSTNAME}/event/{event_id}'
        self._logger.info(f'*** Navigating to{" " + sport_name if sport_name else ""} {event_url}')
        self.device.navigate_to(event_url, event_id=event_id)
        self.site.wait_splash_to_hide(timeout=timeout)
        self.site.close_all_dialogs(async_close=False, timeout=0.5)
        self._logger.info(f'*** Event details url is: {self.device.get_current_url()}')
        if sport_name == 'horse-racing':
            content_state = 'RacingEventDetails'
        elif sport_name == 'greyhound-racing':
            content_state = 'GreyHoundEventDetails'
        elif sport_name == 'tote':
            content_state = 'ToteEventDetails'
        else:
            content_state = 'EventDetails'
        self.site.wait_content_state(state_name=content_state, timeout=timeout)

        stream_and_bet_overlay_sports = ['football', 'horse-racing', 'tennis']
        current_url = self.device.get_current_url()
        is_sport_present = any(sport in current_url for sport in stream_and_bet_overlay_sports)

        if is_sport_present and self.site.wait_for_stream_and_bet_overlay():
            self.site.stream_and_bet_overlay.close_button.click()

        if sport_name and sport_name.lower() == 'horse-racing' and self.site.wait_for_my_stable_onboarding_overlay():
            self.site.my_stable_onboarding_overlay.close_button.click()

    def verify_page_header(self):
        page_title = self.site.contents.header_line.page_title.title
        self.assertEqual(
            page_title,
            self.expected_page_header,
            msg='Page title %s doesn\'t match expected text %s' % (page_title, self.expected_page_header)
        )

    @staticmethod
    def convert_fraction_price_to_decimal(initial_price, round_to=4):
        try:
            format_ = r'^(\d+.+)\/(\d+)$'
            if re.match(format_, initial_price):
                full_price = re.search(format_, initial_price).groups()
                first_number, second_number = full_price
                initial_price = float(first_number) / int(second_number)
            decimal_price = float(Fraction(initial_price))
        except ValueError as e:
            raise GeneralException(e)
        return round(decimal_price, round_to) if round_to else decimal_price

    def set_local_storage_cookies_csp(self, cookie_name, segment):
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=cookie_name)
        cookie_value['segment'] = segment
        data = json.dumps(cookie_value)
        self.device.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", cookie_name, data)
        sleep(5) # In order to reflect in FE

    def get_local_storage_cookie_value(self, cookie_name):
        cookie_value = self.device.driver.execute_script("return localStorage.getItem('%s');" % cookie_name)
        self._logger.debug('*** Cookie "%s" value is "%s"' % (cookie_name, cookie_value))
        return cookie_value if cookie_value else None

    def delete_local_storage_cookie(self, cookie_name):
        self.device.driver.execute_script("return localStorage.removeItem('%s');" % cookie_name)
        self._logger.debug('*** Cookie "%s" is deleted' % cookie_name)

    def set_local_storage_cookie_value(self, cookie_name, value):
        self.device.driver.execute_script(f'localStorage["{cookie_name}"] = "{value}";')

    def get_local_storage_cookie_value_as_dict(self, cookie_name):
        js_value = self.get_local_storage_cookie_value(cookie_name=cookie_name)
        return json.loads(js_value) if js_value else None

    def get_session_storage_cookie_value(self, cookie_name):
        cookie_value = self.device.driver.execute_script("return sessionStorage.getItem('%s');" % cookie_name)
        self._logger.debug('*** Cookie "%s" value is "%s"' % (cookie_name, cookie_value))
        return cookie_value if cookie_value else None

    def get_session_storage_cookie_value_as_dict(self, cookie_name):
        js_value = self.get_session_storage_cookie_value(cookie_name=cookie_name)
        return json.loads(js_value)

    def add_cookie(self, cookie_name, value):
        self.get_session_storage_cookie_value(f'document.cookie = "{cookie_name}={value}";')

    def delete_cookies(self):
        if self.device.browser == 'safari':
            cookies = self.device.driver.get_cookies()
            [self.device.driver.delete_cookie(i['name']) for i in cookies]
        else:
            self.device.driver.delete_all_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.set_local_storage_cookies(self._ls_cookies)

    def get_web_socket_response_by_id(self, response_id: (int, str), delimiter: str = ':::') -> dict:
        """
        DESCRIPTION: This method allows to get Web Socket response info based on required response ID
        :param response_id: expected response ID
        :param delimiter: delimiter for particular WS connection
        :return: Dictionary which contains all WS response info with expected ID
        """
        sleep(0.5)  # so the WS actually contain response on request sent
        logs = self.device.get_performance_log()
        self.assertTrue(logs, msg='No one Network call response found')
        return parse_web_socket_response_by_id(logs=logs, response_id=response_id, delimiter=delimiter)

    def get_web_socket_response_by_url(self, url: str) -> dict:
        """
        DESCRIPTION: This method allows to get Web Socket response info based on required request URL
        :param url: expected request URL
        :return:  Dictionary which contains all URL request info for expected URL
        """
        logs = self.device.get_performance_log()
        self.assertTrue(logs, msg='No one Network call response found')
        return parse_web_socket_response_by_url(logs=logs, url=url)

    def verify_selected_option_on_preferences_page(self, expected_selected_option):
        preferences = self.site.settings
        if expected_selected_option == 'fraction':
            self.assertTrue(preferences.fractional_btn.is_selected(), msg='Fractional option is not active')
            self.assertFalse(preferences.decimal_btn.is_selected(expected_result=False),
                             msg='Decimal option should not be active')
        elif expected_selected_option == 'decimal':
            self.assertFalse(preferences.fractional_btn.is_selected(), msg='Fractional option should not be active')
            self.assertTrue(preferences.decimal_btn.is_selected(expected_result=False),
                            msg='Decimal option is not active')

    def convert_time_to_local(self,
                              date_time_str,
                              ob_format_pattern='%Y-%m-%d %H:%M:%S',
                              ui_format_pattern='%H:%M, Today',
                              future_datetime_format='%d %b',
                              ss_data=False,
                              patch=True,
                              **kwargs):
        if patch:
            # Create Driver object which will invoke set_driver and make it available globally do changes once the bs merged
            self.site

            # Map Python Time to JS Time
            ui_js_format = self.map_python_to_js_time_format(ui_format_pattern)
            future_js_format = self.map_python_to_js_time_format(future_datetime_format)

            # Check if the date_time_str is Today
            is_today = determine_day(date_time_str) == "Today"
            if is_today:
                return format_ss_date_to_ui_date(date_time_str, ui_js_format)
            else:
                return format_ss_date_to_ui_date(date_time_str, future_js_format)

        # If Patch is true then Below Code will not be executed
        timezone = str(get_localzone())
        self._logger.info(f'*** Current timezone is: "{timezone}"')
        # check for summertime due to the openbet/ss are in different timezones
        # by default 0 as we mostly are using OB time from created event
        is_dst = time.localtime().tm_isdst
        dst_time_delta = is_dst if ss_data else 0

        # https://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/
        datetime_obj_naive = datetime.strptime(date_time_str, ob_format_pattern)
        time_zone_name = time.tzname
        self._logger.info(f'*** Time ZONE **** "{time_zone_name}"')

        timezone_ = 'UTC' if tests.location in tests.settings.utc_locations and ss_data else 'GB'
        # note: in case if it will be failing after DST ends, change line above to
        # timezone_ = 'UTC' if tests.location in tests.settings.utc_locations and ss_data and is_dst else 'GB'
        datetime_obj_gb = pytz.timezone(timezone_).localize(datetime_obj_naive)
        if self.use_browser_stack and tests.location == "AWS_GRID":
            datetime_obj_local = datetime_obj_gb.astimezone(pytz.timezone(timezone)) + timedelta(hours=dst_time_delta, minutes=330)
        else:
            datetime_obj_local = datetime_obj_gb.astimezone(pytz.timezone(timezone)) + timedelta(hours=dst_time_delta, minutes=kwargs.get('utcoffset', 0))

        timedelta_obj = (datetime_obj_local - datetime.now(tz=pytz.timezone(timezone)))
        if timedelta_obj.days < 0:
            time_string = datetime_obj_local.strftime(ui_format_pattern)
        elif timedelta_obj.days != 0 or datetime_obj_local.day != datetime.now(tz=pytz.timezone(timezone)).day:
            time_string = datetime_obj_local.strftime(future_datetime_format)
        else:
            time_string = datetime_obj_local.strftime(ui_format_pattern)

        self._logger.info(f'*** Got "{time_string}" date/time from "{date_time_str}"')
        return time_string

    @staticmethod
    def get_event_day(date_time_str: str, format_pattern: str = '%Y-%m-%dT%H:%M:%SZ') -> str:
        """
        Get event day based on startTime attribute from SiteServe response
        :param date_time_str: date time string (event['event']['startTime'])
        :param format_pattern: format pattern that is supported by datetime lib
        :return: TODAY, TOMORROW or FUTURE depending on event's day
        """
        # https://www.saltycrane.com/blog/2009/05/converting-time-zones-datetime-objects-python/
        datetime_obj_naive = datetime.strptime(date_time_str, format_pattern)
        datetime_obj_gb = pytz.timezone('GB').localize(datetime_obj_naive)

        timezone = 'UTC' if tests.location in tests.settings.utc_locations else 'Europe/Kiev'
        datetime_obj_local = datetime_obj_gb.astimezone(pytz.timezone(timezone))
        timedelta_obj = (datetime_obj_local - datetime.now(tz=pytz.timezone(timezone)))
        if timedelta_obj.days == 0 or datetime_obj_local.day == datetime.now(tz=pytz.timezone(timezone)).day:
            return vec.sb.SPORT_DAY_TABS.today
        elif timedelta_obj.days == 1:
            return vec.sb.SPORT_DAY_TABS.tomorrow
        elif timedelta_obj.days > 1:
            return vec.sb.SPORT_DAY_TABS.future
        return ''

    def get_sport_title(self, category_id) -> str:
        """
        Sport title shown on UI Menus. e.g. on Menu Carousel
        """
        sport_categories = self.cms_config.get_sport_categories()
        title = next((sport['imageTitle'] for sport in sport_categories if sport['categoryId'] == category_id), None)
        if not title:
            raise CmsClientException(f'Cannot get Sport title for category id "{category_id}"')
        return title

    def compare_date_time(self, item_time_ui, event_date_time_ob=None, tz_region='GB', format_pattern="%A %-d / %b",
                          **kwargs):
        """
        Where 'event_date_time_ob' named_tuple '*.event_date' got from OB Client
        'item_time_ui' - UI element
        TODAY 'HH:MM AM/PM' for example 8:45 PM, 12:20 PM, 8:30 AM
        TOMORROW (but NOT over 24 hours from now on) - 'HH:MM AM/PM'. For example 8:45 PM, 12:20 PM, 8:30 AM
        TOMORROW (more than 24 hours from now on): DD Mon HH:MM AM/PM. For example 03 Jun 8:45 PM
        FUTURE (Event starting later than tomorrow): DD Mon HH:MM AM/PM. For example 03 Jun 8:45 PM
        """
        dayfirst = kwargs.get('dayfirst', True)
        expected_time = kwargs.get('expected_time')
        if expected_time:
            expected_time_formatted = expected_time.strftime(format_pattern)
            self.assertEqual(item_time_ui, expected_time_formatted,
                             msg='Incorrect date/time shown for item: found "%s", expected "%s"'
                                 % (item_time_ui, expected_time_formatted))
        else:
            date_obj = parse(event_date_time_ob, dayfirst=dayfirst)
            datetime_obj_gb = pytz.timezone('GB').localize(date_obj)  # 2019-01-23 23:39:10+00:00
            timezone = 'UTC' if tests.location in tests.settings.utc_locations else 'Europe/Kiev'
            datetime_obj_local = datetime_obj_gb.astimezone(pytz.timezone(timezone))  # 2019-01-24 01:39:10+02:00
            # getting rid of timezones because till now both localized dates are equal
            gb_date, local_date = datetime.date(datetime_obj_gb), datetime.date(
                datetime_obj_local)  # 2019-01-23  2019-01-24
            format_pattern = '%H:%M, %-d %b' if gb_date < local_date else format_pattern
            event_date = datetime_obj_local.strftime(format_pattern)
            self._logger.info(
                '*** Comparing UI date: "%s" with created OB event date: "%s"' % (item_time_ui, event_date))
            try:
                self.assertEqual(item_time_ui, event_date, msg='UI date "%s" is not equal to created OB event date "%s"'
                                                               % (item_time_ui, event_date))
            except TestFailure as e:
                self._logger.debug('*** Overriding exception %s in %s' % (e, __name__))
                date_ui = parse(item_time_ui, dayfirst=dayfirst)
                date_ob = parse(event_date, dayfirst=dayfirst)
                self.assertEqual(date_ui, date_ob, msg='UI date "%s" is not equal to created OB event date "%s"'
                                                       % (date_ui, date_ob))

    @staticmethod
    def get_date_time_formatted_string(time_format='%Y-%m-%d %H:%M:%S', **kwargs):
        return get_date_time_as_string(time_format=time_format, **kwargs)

    # Sport EDP
    @property
    def my_bets_tab_name(self) -> str:
        """
        Return My Bets tab name
        :return: 'My Bets' tab name
        """
        return 'MY BETS' if self.device_type == 'mobile' else 'My Bets'

    def get_betslip_content(self):
        # if self._betslip_content:
        #     try:
        #         scroll_to = None if self.is_safari else True
        #         self._betslip_loading.is_displayed(timeout=0.5, scroll_to=scroll_to, bypass_exceptions=())
        #         return self._betslip_content
        #     except (StaleElementReferenceException, NoSuchElementException):
        #         self._logger.debug(f'*** Betslip content has refreshed or closed')

        self.__class__._betslip_content = self.site.betslip
        self.__class__._betslip_loading = self._betslip_content.loading_screen
        return self._betslip_content

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(StaleElementReferenceException), reraise=True)
    def get_section(self, section_name: str, timeout: int = 10, expected_result: bool = True):
        """
        This method get page content accordion section based on it's name
        :param section_name: Expected section name
        :param timeout: Time to wait for expected section
        :param expected_result: Expected result
        :return: Instance of found section class
        """
        result = wait_for_result(
            lambda: section_name in self.site.contents.tab_content.accordions_list.items_as_ordered_dict,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Section "{section_name}" is in sections list',
            bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, IndexError, VoltronException)
        )
        try:
            if result:
                section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict[section_name]
                section.scroll_to_we()
                return section
            return None
        except (KeyError, IndexError):
            return None

    def get_output_prices_values(self, section_name, event_id=None):
        event = self.get_event_from_league(event_id=event_id,
                                           section_name=section_name)
        output_prices = event.get_active_prices()
        output_prices_original_values_dict = OrderedDict()
        for selection_name, outputprice in output_prices.items():
            output_prices_original_values_dict[selection_name] = outputprice.outcome_price_text
        return output_prices_original_values_dict

    def verify_user_balance(self, expected_user_balance, page='all', timeout=3, delta=0.01):
        wait_for_haul(5)
        wait_for_result(lambda: abs(float(self.get_balance_by_page(page)) - float(expected_user_balance)) <= delta,
                        name=f'Current amount "{float(self.get_balance_by_page(page))}" to be equal '
                        f'to expected amount "{float(expected_user_balance)}"',
                        timeout=timeout
                        )
        if not isinstance(expected_user_balance, float):
            expected_user_balance = float(expected_user_balance)
        current_balance = self.get_balance_by_page(page)
        self._logger.info(f'*** Current user balance "{current_balance}", '
                          f'expected "{expected_user_balance}" within delta: "{delta}"')
        self.assertAlmostEqual(current_balance, expected_user_balance, delta=delta,
                               msg=f'Current user balance: "{current_balance}" does not match with required: '
                               f'"{expected_user_balance}" within delta "{delta}"')

    def get_balance_by_page(self, page):
        logged_in = None
        balance = 0.00
        try:
            if page == 'quickbet':
                balance = self.site.header.user_balance
                logged_in = True if balance is not None else False
            if page == 'all':
                logged_in = self.site.wait_logged_in(timeout=5)
                balance = self.site.header.user_balance
            elif page == 'betslip':
                logged_in = self.site.wait_logged_in(timeout=3, login_criteria='betslip_balance')
                balance = self.get_betslip_content().header.user_balance
            elif page == 'betreceipt':
                logged_in = self.site.wait_logged_in(timeout=3, login_criteria='betreceipt_balance')
                balance = self.site.bet_receipt.user_header.user_balance
        except NotImplementedError as e:
            if self.device_type not in ('desktop',):
                raise VoltronException(e)
            self._logger.warning(f'*** Got exception {e}, suppose it\'s desktop execution')
            logged_in = self.site.wait_logged_in(timeout=3)
            balance = self.site.header.user_balance
        except (VoltronException, AttributeError) as e:
            self._logger.error(f'*** User is not logged in because of exception {e}')
            logged_in = False
        self.assertTrue(logged_in, msg=f'User is not logged in, current page is {page}')
        return balance

    def verify_betslip_counter_change(self, expected_value):
        result = wait_for_result(lambda: self.get_betslip_counter_value() == str(expected_value),
                                 name=f'Betslip counter to change from "{self.get_betslip_counter_value()} to "{str(expected_value)}"',
                                 timeout=tests.settings.betslip_counter_timeout)
        self.assertTrue(result, msg=f'Current Betslip counter: "{self.get_betslip_counter_value()}" '
                                    f'does not match with required: "{str(expected_value)}"')

    def get_betslip_counter_value(self):
        return self.site.header.bet_slip_counter.counter_value

    def check_promotion_dialog_appearance_and_close_it(self, expected_title):
        dialog = self.site.wait_for_dialog(expected_title)
        self.assertTrue(dialog, msg=f'{expected_title} dialog is not shown')
        dialog.default_action()
        self.assertTrue(dialog.wait_dialog_closed(), msg=f'{dialog.__class__.__name__} was not closed')

    def check_each_way_terms_format(self, each_way_terms, format=vec.regex.EXPECTED_EACH_WAY_FORMAT, future_tab=False):
        """
        This method check each way terms format
        :param each_way_terms: Expected section name
        :param format: Each way format
        :param future_tab: E/W format is different on Future tab for horse events (by default - False)
        """
        if future_tab:
            each_format_way = format if self.device_type != 'desktop' else vec.regex.EXPECTED_EACH_WAY_FORMAT_DESKTOP_FUTURE
        else:
            each_format_way = format
        self.assertRegexpMatches(each_way_terms, each_format_way,
                                 msg=f'Each Way terms "{each_way_terms}" not matching pattern "{each_format_way}"')

    def check_each_way_terms_correctness(self, each_way_terms, expected_each_way_terms, **kwargs):
        extra_place_format = kwargs.get('extra_place', False)
        betslip = kwargs.get('betslip', False)
        if extra_place_format:
            self.assertRegex(each_way_terms, vec.regex.EXPECTED_EACH_WAY_FORMAT_EXTRA_PLACE)
            ew = re.search(vec.regex.EXPECTED_EACH_WAY_FORMAT_EXTRA_PLACE, each_way_terms).groups()
            ew_odds, ew_places = ew
        elif betslip:
            self.assertRegex(each_way_terms, vec.regex.EXPECTED_EACH_WAY_FORMAT_BET_RECEIPT)
            ew = re.search(vec.regex.EXPECTED_EACH_WAY_FORMAT_BET_RECEIPT, each_way_terms).groups()
            ew_odds, ew_places = ew
        else:
            self.assertRegex(each_way_terms, vec.regex.EXPECTED_EACH_WAY_FORMAT)
            ew = re.search(vec.regex.EXPECTED_EACH_WAY_FORMAT, each_way_terms).groups()
            _, ew_odds, _, _, ew_places = ew
        self._logger.debug('*** Each way odds "%s", places "%s"' % (ew_odds, ew_places))
        expected_odds = '%s/%s' % (expected_each_way_terms['ew_fac_num'], expected_each_way_terms['ew_fac_den'])
        self.assertEqual(ew_odds, expected_odds,
                         msg='Each Way odds "%s" are not the same as expected "%s"'
                             % (ew_odds, expected_odds))
        expected_ew_places = '-'.join([str(x) for x in range(1, int(expected_each_way_terms['ew_places']) + 1)])
        self.assertEqual(ew_places, expected_ew_places,
                         msg='Each Way places "%s" is not the same as expected "%s"'
                             % (ew_places, expected_ew_places))

    def get_filtered_widget_name(self, cms_type: str, column: str = None) -> str:
        """
        :param cms_type: field from CMS API (eg. 'betslip', 'inplay')
        :param column: field from CMS API (eg. 'rightColumn', 'leftColumn') - optional
        :return: item from CMS widgets filtered by type and column
        """
        widgets_from_cms = self.cms_config.get_widgets()
        output = []
        for item in widgets_from_cms:
            if not column:
                if item['type'] == cms_type:
                    output.append(item['title'].upper())
            else:
                if item['type'] == cms_type:
                    if item['columns'] in ['both', column]:
                        output.append(item['title'].upper())
                    else:
                        raise CmsClientException(f'Wrong CMS Offers column for "{item["type"]}". Expected "{column}" got "{item["columns"]}"')
        if len(output) == 0:
            raise CmsClientException('Can not find given type in CMS widgets')
        if len(output) > 1:
            raise CmsClientException('In CMS there is more than one widget of a given type and column')
        return output[0]

    def get_widget(self, cms_type: str, column: str = None):
        """
        :param cms_type: field from CMS API (eg. 'betslip', 'inplay')
        :param column: field from CMS API (eg. 'rightColumn', 'leftColumn') - optional
        :return: widget
        """
        name = self.get_filtered_widget_name(cms_type=cms_type, column=column)
        widgets = self.site.right_column.items_as_ordered_dict
        self.assertTrue(widgets, msg='Right Column widgets are not displayed')
        widget = widgets.get(name)
        if widget is not None:
            return widget
        raise VoltronException('{0} widget was not found among {1} widgets'.format(name, ', '.join(widgets.keys())))

    def get_ribbon_tab_name(self, internal_id: str, raise_exceptions: bool = True) -> str:
        """
        :param internal_id: field from CMS API - Module Ribbon Tabs Page
        :param raise_exceptions: if raise exceptions on fails or not
        :return: field title for internalId
        """
        tab_name = self.cms_config.module_ribbon_tabs.get_tab_name(internal_id=internal_id, raise_exceptions=raise_exceptions)
        if internal_id == self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races:
            return tab_name.title() if self.device_type == 'desktop' and self.brand != 'ladbrokes' else tab_name.upper()
        elif internal_id == self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured:
            return vec.sb_desktop.FEATURED_MODULE_NAME if self.device_type == 'desktop' else tab_name.upper()
        else:
            return tab_name.upper()

    def get_visible_sport_tabs(self, category_id: int) -> list:
        """
        :param category_id: sport category id
        :return: tabs list
        """
        tabs_data = self.cms_config.get_sport_config(category_id=category_id).get('tabs')
        return [tab for tab in tabs_data if tab.get('hidden') is False]

    def get_sport_tab_name(self, name: str, category_id: int, raise_exceptions: bool = True) -> str:
        """
        :param name: field from CMS API - Sport Tabs Page
        :param category_id: sport category id
        :param raise_exceptions: whether raise exception on fail or not
        :return: field label for internal tab name
        """
        if name == 'jackpot' and category_id not in (self.ob_config.football_config.category_id,):
            self._logger.warning('Jackpot is only for football')
            return ''
        tabs_data = self.cms_config.get_sport_config(category_id=category_id).get('tabs')
        if not tabs_data:
            raise CmsClientException(f'No tabs found for sport category id: "{category_id}"')

        sport_tab_name = None
        sport_tab = next((tab for tab in tabs_data if tab.get('name') == name), '')

        if sport_tab and not sport_tab.get('hidden'):
            sport_tab_name = sport_tab.get('label').upper()
        else:
            raise CmsClientException(f'{name} is set to hidden in cms')
        if not sport_tab_name and raise_exceptions:
            available_tabs = [tab.get('name') for tab in tabs_data]
            raise CmsClientException(f'"{name}" is not present in "{available_tabs}" for category "{category_id}"')
        return sport_tab_name

    def get_build_info_json(self):
        url = f'https://{tests.HOSTNAME}/buildInfo.json'
        r = do_request(method='GET', url=url)
        return r

    def is_tab_present(self, tab_name: str, category_id: int) -> bool:
        """
        Verifies if tab should be present on specific SLP based on CMS config
        :param tab_name: tab name, based on tab 'name' parameter in CMS
               (refer to cms.SPORT_TABS_INTERNAL_NAMES in voltron/environments/constants/base/cms.py)
        :param category_id: id of sport category (e.g. 16 for football on coral/tst2)
        :return: True/False
        """
        visible_tabs = self.get_visible_sport_tabs(category_id=category_id)
        available_tabs = [tab.get('name') for tab in visible_tabs]
        return tab_name in available_tabs

    def check_sport_configured(self, category_id: int):
        """
        Verifies if sport is configured in CMS
        :param category_id: id of sport category (e.g. 16 for football)
        """
        sport_config = self.cms_config.get_sport_config(category_id=category_id)
        request = sport_config.get('config').get('request')
        if not request.get('isActive') and request.get('siteChannels') == 'M':
            tabs_data = sport_config.get('tabs')
            active_tabs = [tab for tab in tabs_data if not tab.get('hidden')]
        else:
            raise CmsClientException(f'Sport is not configured in CMS for sport category id: "{category_id}"')
        if not active_tabs:
            raise CmsClientException(f'All tabs are hidden in CMS for sport category id: "{category_id}"')

    def get_promotion_details_from_cms(self, event_level_flag: str, market_level_flag: str) -> dict:
        """
        Gets promotion details from CMS
        :param event_level_flag: one of EVFLAG_DYW, EVFLAG_BBL, EVFLAG_EPR, EVFLAG_FI
        :param market_level_flag: one of MKTFLAG_DYW, MKTFLAG_BBAL, MKTFLAG_EPR, MKTFLAG_FIN
        :return: dictionary with promo details
        """
        promotions = self.cms_config.get_promotions()
        if not promotions:
            raise CmsClientException('No promotions available')
        promo_details = None
        end = ''
        for promotion in promotions:
            if not promotion.get('isSignpostingPromotion'):
                continue
            if not promotion.get('eventLevelFlag') and not promotion.get('marketLevelFlag'):
                continue
            if promotion['eventLevelFlag'] == event_level_flag and promotion['marketLevelFlag'] == market_level_flag:
                start = datetime.strptime(promotion['validityPeriodStart'], '%Y-%m-%dT%H:%M:%SZ')
                end = datetime.strptime(promotion['validityPeriodEnd'], '%Y-%m-%dT%H:%M:%SZ')
                if start <= datetime.utcnow() <= end:
                    if promotion['popupTitle'] is None:
                        raise CmsClientException('Can\'t get Promotion Popup title')
                    else:
                        promo_details = promotion
                        break
                else:
                    continue
        if not promo_details:
            raise CmsClientException(f'Promotion with event level flag "{event_level_flag}" and market level flag '
                                     f'"{market_level_flag}" not found or promotion period has expired: "{end}"')

        return promo_details

    def wait_for_price_update_from_featured_ms(self, event_id: str, selection_id: str, delimiter='42/0,', timeout=40,
                                               poll_interval=0.5, **kwargs) -> dict:
        """
        Waits for price updates for specific selection from Featured MS
        :param event_id: id of event
        :param selection_id: id of selection
        :param delimiter: message delimiter in WS
        :param timeout: timeout for waiting for price updates
        :param poll_interval: interval for polling for changes
        :return: WS message or False
        """
        price = kwargs.get('price')

        result = wait_for_result(
            lambda: get_live_updates_for_event_on_featured_ms(event_id=event_id, delimiter=delimiter,
                                                              selection_id=selection_id, price=price),
            name=f'Price update for event id "{event_id}", selection id "{selection_id}"',
            timeout=timeout,
            poll_interval=poll_interval,
            bypass_exceptions=(IndexError, KeyError, TypeError))

        return result

    def wait_for_price_update_from_live_serv(self, selection_id: str, delimiter='42', timeout: float = 60,
                                             poll_interval: float = 0.5, **kwargs) -> dict:
        """
        Waits for price updates for specific selection
        :param selection_id: id of selection
        :param delimiter: message delimiter in WS
        :param timeout: timeout for waiting for price updates
        :param poll_interval: interval for polling for changes
        :return: WS message or False
        """
        price = kwargs.get('price')
        multi_update = kwargs.get('multi_update')
        preserve_option = kwargs.get('preserve')
        if len(selection_id) < 9:
            selection_id = f'0{selection_id}'
        result = wait_for_result(lambda: get_live_serve_updates(delimiter=delimiter, selection_id=selection_id,
                                                                price=price, multi_update=multi_update, preserve=preserve_option),
                                 name=f'Price update for selection id "{selection_id}"',
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=(IndexError, KeyError, TypeError))
        return result

    def wait_for_event_market_selection_state_update_from_live_serv(self, delimiter='42', timeout: float = 50,
                                                                    poll_interval: float = 0.5, **kwargs) -> dict:
        """
        Waits for event state updates
        :param delimiter: message delimiter in WS
        :param timeout: timeout for waiting for event/market/selection updates
        :param poll_interval: interval for polling for changes
        :return: WS message or False
        """
        result = wait_for_result(lambda: get_live_serve_updates(delimiter=delimiter, **kwargs),
                                 name=f'State update for Event/market/selection id "{kwargs}"',
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=(IndexError, KeyError, TypeError))
        return result

    def verify_selections_displayed(self, tab, selections: list, expected_result: bool = True) -> dict:
        """
        Verifies if bets for given selections are presents on <MyBets> tabs
        :param tab: specifies tab
        :param selections: specifies selections
        :param expected_result: Specifies the result of selections presence
        :return: dict of corresponding bet legs if bets are found successfully
        """
        sections = tab.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections displayed in "Open Bets" tab')

        bet_legs_dict = {}
        for _, section in list(sections.items()):
            bet_legs = section.items_as_ordered_dict
            for index in range(len(bet_legs.keys())):
                bet_leg_name, bet_leg = list(bet_legs.items())[index]
                bet_leg_name = bet_leg_name.split(' - ')[0]
                if bet_leg_name in selections:
                    bet_legs_dict[bet_leg_name] = bet_leg

        for index in range(len(bet_legs_dict.keys())):
            if expected_result:
                self.assertIn(selections[index], bet_legs_dict.keys(),
                              msg=f'"{selections[index]}" is not found in "{bet_legs_dict.keys()}"')
            else:
                self.assertNotIn(selections[index], bet_legs_dict.keys(),
                                 msg=f'"{selections[index]}" is found in "{bet_legs_dict.keys()}"')
                bet_legs_dict = {}

        return bet_legs_dict

    def is_settled(self, event_id, outcome_id):
        """
        This function is getting actual status of settled outcome
        :param event_id: ID of event
        :param outcome_id: ID of selection to check if it is settled
        """
        query_debug_include_hidden_fields = self.ss_query_builder.add_filter(debug_filter())
        event_data = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id,
                                                               query_builder=query_debug_include_hidden_fields)
        for outcome in event_data[0]['event']['children'][0]['market']['children']:
            if str(outcome['outcome']['id']) == str(outcome_id):
                return outcome['outcome']['isSettled']

    def result_event(self, selection_ids, market_id, event_id, **kwargs):
        if not isinstance(selection_ids, (list, KeysView, ValuesView)):
            selection_ids = [selection_ids]
        for selection_id in selection_ids:
            self.ob_config.result_selection(selection_id=selection_id, market_id=market_id, event_id=event_id,
                                            wait_for_update=False, **kwargs)
        for selection_id in selection_ids:
            self.ob_config.confirm_result(selection_id=selection_id, market_id=market_id, event_id=event_id,
                                          wait_for_update=False, **kwargs)
        for selection_id in selection_ids:
            self.ob_config.settle_result(selection_id=selection_id, market_id=market_id, event_id=event_id,
                                         wait_for_update=False, **kwargs)
            result = wait_for_result(lambda: self.is_settled(event_id=event_id, outcome_id=selection_id) == 'true',
                                     poll_interval=10, timeout=60,
                                     name='Settle status to become "true"')
            self.assertTrue(result, msg=f'Status for "{self.team1}" outcome was not updated')

    @classmethod
    def suspend_old_events(cls, class_ids):
        end_date = f'{get_date_time_as_string(hours=-4, time_format="%Y-%m-%dT%H:%M")}:00.000Z'
        ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=cls.brand)
        filters = query_builder().add_filter(translation_lang()) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A'))

        resp = ss_req.ss_event_to_outcome_for_class(query_builder=filters)
        for event in resp:
            cls.get_ob_config().change_event_state(event_id=event['event']['id'], active=False, displayed=True)

    def get_favourites_enabled_status(self) -> bool:
        """
        Method to check if Favourites functionality is enabled on CMS
        :return: Favourites Enabled status for device type
        """
        system_configuration = self.get_initial_data_system_configuration()
        favourites = system_configuration.get('Favourites')
        if not favourites:
            favourites = self.cms_config.get_system_configuration_item('Favourites')
        if not favourites:
            raise CmsClientException('"Favourites" section is not added to System Config on CMS')
        return favourites[f'displayOn{self.device_type.title()}']

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)),
           reraise=True)
    def get_inplay_sport_menu_items(self):
        return self.site.inplay.inplay_sport_menu.items_as_ordered_dict

    def get_default_tab_name_on_sports_edp(self, event_id):
        if self.brand != 'ladbrokes':
            response = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=self.ss_query_builder)
            markets = response[0]['event']['children']
            for market in markets:
                if market.get('market', {}).get('templateMarketName', '') in ['Match Result', 'Match Betting']:
                    if 'Main,' in market.get('market', {}).get('collectionNames', ''):
                        return vec.siteserve.EXPECTED_MARKET_TABS.main
                    elif 'Main Markets,' in market.get('market', {}).get('collectionNames', ''):
                        return vec.siteserve.EXPECTED_MARKET_TABS.main_markets
                    else:
                        return vec.siteserve.EXPECTED_MARKET_TABS.all_markets
        else:
            return vec.siteserve.EXPECTED_MARKET_TABS.all_markets

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(StaleElementReferenceException), reraise=True)
    def get_event_from_league(self, event_id=None, section_name=None, raise_exceptions=True, **kwargs):
        """
        This method get event from league by event id
        :param event_id: Openbet/SiteServe ID for event
        :param section_name: Expected section name
        :param raise_exceptions: whether is to raise TestFailure exception in case event is not found
        :return: SportEventListItem event object
        """
        if not event_id:
            category_id = kwargs.get('category_id', 16)
            active_event = self.get_active_events_for_category(category_id=category_id)[0]
            event_id = active_event['event']['id']
            section_name = self.get_accordion_name_for_event_from_ss(active_event)
        inplay_section = kwargs.get('inplay_section')

        if not inplay_section:
            try:
                container = self.site.contents.tab_content.accordions_list
            except Exception:
                container = self.site.sports_page.tab_content.accordions_list

        elif 'LIVE' in inplay_section.upper() or 'UPCOMING' in inplay_section.upper():
            if self.device_type == 'desktop':
                self.site.contents.tab_content.grouping_buttons.click_button(inplay_section)
                container = self.site.contents.tab_content.accordions_list
            else:
                tab_content = self.site.contents.tab_content
                container = tab_content.live_now if 'LIVE' in inplay_section.upper() else tab_content.upcoming
        else:
            self._logger.warning(f'*** In Play section type "{inplay_section}" is not provided, returning default accordion list')
            container = self.site.contents.tab_content.accordions_list

        event = container.get_event_from_league_by_event_id(
            league=section_name, event_id=event_id, raise_exceptions=raise_exceptions)

        if raise_exceptions:
            self.assertIsNotNone(event, msg=f'Event with id "{event_id}" was not found in section: "{section_name}"')
            self.__class__.event_name_on_sports_page = event.event_name
            self._logger.debug(f'*** Event name on <Sport> page: {self.event_name_on_sports_page}')
        return event

    def get_freebet_redemption_name(self, level='any'):
        """
        Gets level of freebet
        :param level: one of any, selection, class, type, event, market
        :return: redemption name (level)
        """
        freebets = self.ob_config.backend.ob.freebets
        return freebets.get(level, {}).get('name', '')

    @property
    def freebet_name_template(self):
        """
        Returns freebet offer name
        :return: freebet offer name
        """
        freebets = self.ob_config.backend.ob.freebets
        return freebets.get('general_offer', {}).get('name', '')

    def get_freebet_name(self, value, **kwargs):
        """
        Gets freebet full name including redemption name (level) and value
        :param value: freebet value
        :param kwargs: can accept custom template_name and redemption_name
        :return: full name of freebet
        """
        template_name = kwargs.get('template_name', self.freebet_name_template)
        redemption_name = kwargs.get('redemption_name', self.get_freebet_redemption_name())
        return f'£{value} {template_name} ({redemption_name})'

    def verify_bet_in_open_bets(self, bet_type, event_name, bet_in_open_bets=True):
        try:
            bet_name, _ = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type, event_names=event_name)
            if bet_in_open_bets:
                self.assertTrue(event_name in bet_name, msg=f'*** "{event_name}" bet not found in the openbets')
            else:
                self.assertFalse(event_name in bet_name, msg=f'***"{event_name}" bet is present in openbets')
        except VoltronException as e:
            self._logger.warning(f'*** {e} ***')

    def rgba_to_hex(self, rgba_color):
        """
        :param rgba_color:requires rgba color in format of 'rgba(0,0,0,1)'
        :return: hex format color will be returned
        """
        rgba_color = re.search(r'\(.*\)', rgba_color).group(0).replace(' ', '').lstrip('(').rstrip(')')
        [r, g, b] = [int(x) for x in rgba_color.split(',')[:3]]
        # check if in range 0~255
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255

        r = hex(r).lstrip('0x')
        g = hex(g).lstrip('0x')
        b = hex(b).lstrip('0x')
        # re-write '7' to '07'
        r = (2 - len(r)) * '0' + r
        g = (2 - len(g)) * '0' + g
        b = (2 - len(b)) * '0' + b

        hex_color = '#' + r + g + b
        return hex_color

    def block_unblock_request_domain(self, cmd=None, params={}):
        """
        :param cmd: devtools protocol command/s
        :param params: Required Domain URL/s as a dict

        """
        resource = "/session/%s/chromium/send_command_and_get_result" % self.device.driver.session_id
        url = self.device.driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = self.device.driver.command_executor._request('POST', url, body)
        return response.get('value')

    def get_timeline_campaign_id(self):
        """
        return: timeline campaign
        """
        all_timeline_campaigns = self.cms_config.get_timeline_campaign()
        timeline_campaign = next((module for module in all_timeline_campaigns if
                                  module.get('status') == "LIVE" and module.get(
                                      'displayFrom') <= dt.datetime.utcnow().isoformat() <= module.get(
                                      'displayTo')), None)
        if not timeline_campaign:
            timeline_campaign = self.cms_config.add_timeline_campaign(campaign_name="auto_test_spotlight_campaign",
                                                                      status="LIVE")
        timeline_campaign_id = timeline_campaign.get('id')
        return timeline_campaign_id

    def get_eventid_selectionid(self):
        """
        return: event and selection ids for spotlight timeline campaign
        """
        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.horseracing_config.category_id)
        response = None
        for id in class_ids:
            response = self.cms_config.spotlight_related_events(class_id=id)
            if not response['typeEvents']:
                continue
            else:
                break

        if not response['typeEvents']:
            raise CmsClientException('No spotlight events available')

        event_id = response['typeEvents'][0]['events'][0]['id']
        selection_id = response['typeEvents'][0]['events'][0]['children'][0]['market']['children'][00]['outcome']['id']
        return event_id, selection_id

    def create_question_engine_quiz(self, pop_up=False):
        """
        @param pop_up: True or False
        """
        if self.brand == 'bma':
            quiz = self.cms_config.check_update_and_create_question_engine_quiz()
            quiz_id = quiz['id']
        else:
            lad_quiz = self.cms_config.check_update_and_create_question_engine_quiz()
            lad_quiz['quizConfiguration']['showSubmitPopup'] = False
            lad_quiz['quizConfiguration']['showExitPopup'] = False
            lad_quiz['quizConfiguration']['showSplashPage'] = False
            lad_quiz['quizConfiguration']['showEventDetails'] = False
            lad_quiz['quizConfiguration']['showProgressBar'] = False
            lad_quiz['quizConfiguration']['showQuestionNumbering'] = False
            lad_quiz['quizConfiguration']['showSwipeTutorial'] = False
            lad_quiz['quizConfiguration']['showPreviousAndLatestTabs'] = False
            quiz_id = lad_quiz['id']
            quiz_title = lad_quiz['title']
            quiz = self.cms_config.update_question_engine_quiz(quiz_id=quiz_id, title=quiz_title, payload=lad_quiz)
        if pop_up:
            quiz_pop_up = self.cms_config.create_question_engine_pop_up(quiz_id=quiz_id)
            return (quiz, quiz_pop_up)
        return quiz

    def update_spotlight_events_price(self, class_id=223, **kwargs):
        """
        @param class_id: Sport class ID
        """
        increased_price = kwargs.get('increased_price', '1/2')
        events_response = self.cms_config.spotlight_related_events(class_id)
        sport_event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                       category_id=self.ob_config.horseracing_config.category_id,
                                       class_id=class_id,
                                       type_id=events_response['typeEvents'][0]['typeId'])

        for event in range(len([events_response['typeEvents'][0]['events']][0])):
            for market in range(len([events_response['typeEvents'][0]['events']][0][event]['markets'])):
                if [events_response['typeEvents'][0]['events']][0][event]['markets'][market]['templateMarketName'] == 'Win or Each Way':
                    if ([events_response['typeEvents'][0]['events']][0][0]['markets'][0]['isLpAvailable'] is not True) or ([events_response['typeEvents'][0]['events']][0][0]['markets'][0]['isSpAvailable'] is not True) or ([events_response['typeEvents'][0]['events']][0][0]['markets'][0]['isGpAvailable'] is not True):
                        sport_event.update_market_settings(
                            market_id=[events_response['typeEvents'][0]['events']][0][event]['markets'][market]['id'],
                            event_id=[events_response['typeEvents'][0]['events']][0][event]['markets'][market][
                                'eventId'],
                            market_template_id=[events_response['typeEvents'][0]['events']][0][event]['markets'][market][
                                'templateMarketId'], lp_avail='Y', sp_avail='Y', gp_avail='Y')
                        for outcome in range(
                                len([events_response['typeEvents'][0]['events']][0][event]['markets'][market]['outcomes'])):
                            self.ob_config.change_price(selection_id=[events_response['typeEvents'][0]['events']][0][event]['markets'][market]['outcomes'][outcome]['id'],
                                                        price=increased_price)

    def create_eventhub(self, **kwargs):
        """
        Create a new EventHub module in the CMS configuration.

        This method creates a new EventHub module with a unique index number and associated tab in module ribbon tabs.

        Args:
            **kwargs: Additional keyword arguments to configure the EventHub module.
            For example: you can send 'title' in this method argument to configure the desired name.

        Returns:
            dict: Details of the created EventHub module tab.

        """
        # Retrieve all existing event hubs from the CMS 'event hub tab'.
        existing_event_hubs = self.cms_config.get_event_hubs()

        # Get all the data from CMS 'module ribbon tabs'
        all_module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data

        # Define the maximum number of allowed event hubs
        max_allowed_event_hubs = 6

        # Check if the number of existing event hubs exceeds the maximum allowed
        if len(existing_event_hubs) >= max_allowed_event_hubs:

            # Extract internal IDs of EventHub tabs
            all_module_ribbon_tab_event_hub_indexes = [
                tab['internalId'].replace('tab-eventhub-', '')
                for tab in all_module_ribbon_tabs
                if tab.get('directiveName') == 'EventHub'
            ]

            # Extract IDs of inactive EventHub tabs
            all_inactive_eventhub_indexes = [
                tab['internalId'].replace('tab-eventhub-', '')
                for tab in all_module_ribbon_tabs
                if tab.get('directiveName') == 'EventHub'
                   and (not tab.get('visible')
                        or dt.datetime.utcnow().isoformat() > tab.get('displayTo'))
            ]

            # Delete inactive EventHub modules
            for event_hub in existing_event_hubs:
                tab_index_number = str(event_hub.get('indexNumber'))
                if tab_index_number not in all_module_ribbon_tab_event_hub_indexes or tab_index_number in all_inactive_eventhub_indexes:
                    self.cms_config.delete_event_hub_module(event_hub.get('id'))
                    break  # Only delete one module if multiple conditions are met


        # Retrieve existing event hubs from the CMS configuration. Extracting index numbers of existing event hubs.
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

        # Find the next available index number (from 1 to 19) that is not already in use.
        self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)

        # Create a new event hub with the determined index number.
        self.cms_config.create_event_hub(index_number=self.index_number)

        # Define an internal ID for the event hub tab.
        internal_id = f'tab-eventhub-{self.index_number}'

        # Create a tab for the event hub in module ribbon tabs with specified details.
        return self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=self.index_number,
                                                                           display_date=True, **kwargs)
    def get_module_data_by_directive_name_from_cms(self, directiveName: str, expected_tab_display_name=None, expected_result=True):
        """
        Check if a specific tab is available on the homepage in CMS.

        Args:
            expected_tab_display_name (str): The expected display name of the tab.
            directiveName (str): The directive name associated with the tab.
            expected_result (bool, optional): Whether the tab is expected to be available. Defaults to True.

        Returns:
            dict or None: Returns the details of the tab if found, or None if not found.

        Raises:
            ValueError: If the 'directiveName' argument is not one of the expected values.

        """
        if expected_tab_display_name:
            expected_tab_display_name = expected_tab_display_name.upper()

        expected_directive_name_list = ['Featured', 'InPlay', 'NextRaces', 'EventHub', 'Coupons', 'LiveStream', 'BuildYourBet', 'Multiples', 'TopBets']
        if not directiveName in expected_directive_name_list:
            raise ValueError("Argument of 'directiveName' is not as expected")

        def is_within_display_range(tab, expected_result=True):
            if directiveName == 'EventHub':
                current_time = dt.datetime.utcnow().isoformat()
                condition_result = tab.get('displayFrom') <= current_time <= tab.get('displayTo')
                return condition_result if expected_result else not condition_result
            else:
                return True

        # getting tabs of module ribbon tab from cms and checking if any of them are event hub
        module_ribbon_tabs_cms = self.cms_config.module_ribbon_tabs.all_tabs_data
        tabs_cms = [tab for tab in module_ribbon_tabs_cms if
                                   tab['visible'] is expected_result and
                                   tab['directiveName'] == directiveName and
                                   is_within_display_range(tab=tab, expected_result=expected_result)]
        # if the 'tab' argument is not sent then return the list of tabs with expected directive name.
        if not expected_tab_display_name:
            return tabs_cms

        # getting data of the expected tab
        return next((tab for tab in tabs_cms if tab['title'].upper() == expected_tab_display_name), None)

    def categorize_date(self, input_date_str):
        # Convert the input string to a datetime object
        input_date = datetime.strptime(input_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=None)
        # Get the current date
        current_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        # Calculate the difference between the input date and the current date
        time_difference = input_date - current_date
        # Compare the date with today, tomorrow, or future
        if time_difference.days == 0:
            return "TODAY"
        elif time_difference.days == 1:
            return "TOMORROW"
        elif time_difference.days > 1:
            return "FUTURE"
        else:
            return "past"
