import random
from collections import OrderedDict

from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

import tests_ios_fully_native_regression as tests
from native_ios.utils.exceptions.siteserve_exception import SiteServeException
from tests_ios_fully_native_regression.base_test import BaseTest


class Common(BaseTest):
    all_selections = {}
    eventID = None
    marketID = None
    selection_ids = OrderedDict()

    # Time format patterns
    ob_format_pattern = '%Y-%m-%dT%H:%M:%SZ'
    time_format_pattern = '%H:%M - %d %b'

    @property
    def end_date(self):
        """
        Mobile view default SiteServe filter on UI includes today + tomorrow events, Desktop - only today events
        :return: end date string
        """
        days = 1
        end_date = f'{get_date_time_as_string(days=days)}T00:00:00.000Z'
        return end_date

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
        if kwargs.get('all_available_events'):
            return found_events
        if len(found_events) < number_of_events and raise_exceptions:
            raise SiteServeException(
                f'No enough active events for category id "{category_id}"')
        random.shuffle(found_events)
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
