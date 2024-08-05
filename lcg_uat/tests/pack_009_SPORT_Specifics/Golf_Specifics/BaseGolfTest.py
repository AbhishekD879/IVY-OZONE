import random
import tests
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments.constants.base.siteserve_drilldown_tags import SS_MARKET_LEVEL_DRILLDOWN_TAGS
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tenacity import retry_if_exception_type, stop_after_attempt, retry
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter


class BaseGolfTest(BaseBetSlipTest):
    lucky_dip_config = {
        "markets": [('lucky_dip', {'cashout': False, 'disp_order': -999})],  # Config for ob_config_yaml
        "tournament_sort_code": "TNMT",
        "event_level_cashout": False,
        "default_market_config": {
            "market_name": "|Outright|",
            "market_template_id": "357478"
        }
    }
    created_event = None

    @property
    def golf_class_ids(self):
        return self.get_class_ids_for_category(category_id=self.golf_category_id)

    @property
    def golf_category_id(self):
        return self.ob_config.golf_config.category_id

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(SiteServeException), reraise=True)
    def get_active_lucky_dip_events(self, number_of_events=1, all_available_events=False,
                                    raise_exceptions: bool = True,category_id=18):
        ss_config = SiteServeRequests(env=tests.settings.backend_env, class_id=self.get_class_ids_for_category(category_id=category_id), brand=self.brand,
                                      category_id=category_id)
        lucky_dip_events_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES, OPERATORS.CONTAINS,
                                      SS_MARKET_LEVEL_DRILLDOWN_TAGS.LUCKY_DIP_DRILLDOWN)) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A'))

        found_events = []
        resp = ss_config.ss_event_to_outcome_for_class(query_builder=lucky_dip_events_filter)
        self._logger.info(
            f'*** Found {len(resp)} event(s) for category {category_id} and classes {self.get_class_ids_for_category(category_id=category_id)}')

        for event in resp:
            if event.get('event') and event['event'].get('children'):
                markets = event['event']['children']
                for market in markets:
                    if market.get('market') and market['market'].get('children'):
                        for outcome in market['market']['children']:
                            if outcome['outcome'].get('children'):
                                for child in outcome['outcome']['children']:
                                    if child.get('price'):
                                        found_events.append(event)
                                    break
                            break

        if not found_events and raise_exceptions:
            raise SiteServeException(
                f'No active events found for category id "{category_id}" with luckydip market')
        if all_available_events:
            return found_events
        if len(found_events) < number_of_events and raise_exceptions:
            raise SiteServeException(
                f'No enough active events for category id "{category_id}" with luckydip market')
        random.shuffle(found_events)
        return found_events[:number_of_events]

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(SiteServeException), reraise=True)
    def get_active_golf_events(self, number_of_events=1, all_available_events=False,
                               raise_exceptions: bool = True, **kwargs):
        ss_config = SiteServeRequests(env=tests.settings.backend_env, class_id=self.golf_class_ids, brand=self.brand)
        events_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE)) \
            .add_filter(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A'))

        additional_filters = kwargs.get('additional_filters')

        if additional_filters:
            if not isinstance(additional_filters, (list, tuple)):
                additional_filters = [additional_filters]
            for filter_ in additional_filters:
                events_filter.add_filter(filter_)

        found_events = []
        resp = ss_config.ss_event_to_outcome_for_class(query_builder=events_filter)
        self._logger.info(
            f'*** Found {len(resp)} event(s) for category {self.golf_category_id} and classes {self.golf_class_ids}')

        for event in resp:
            if event.get('event') and event['event'].get('children'):
                markets = event['event']['children']
                for market in markets:
                    for outcome in market['market']['children']:
                        if outcome['outcome'].get('children'):
                            for child in outcome['outcome']['children']:
                                if child.get('price'):
                                    found_events.append(event)
                                break
                        break

        if not found_events and raise_exceptions:
            raise SiteServeException(f'No active events found for category id "{self.golf_category_id}"')
        if all_available_events:
            return found_events
        if len(found_events) < number_of_events and raise_exceptions:
            raise SiteServeException(
                f'No enough active events for category id "{self.golf_category_id}"')
        random.shuffle(found_events)
        return found_events[:number_of_events]

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(SiteServeException), reraise=True)
    def get_selected_golfer_name_in_ob_config(self, event):
        golfer_name = None
        markets = event['event']['children']
        for market in markets:
            if SS_MARKET_LEVEL_DRILLDOWN_TAGS.LUCKY_DIP_DRILLDOWN in market['market']['drilldownTagNames']:
                golfer_name = market['market']['children'][0]['outcome']['name']
                break
        if not golfer_name:
            raise SiteServeException('Random Golfer Name is Not Selected in Open Bet(OB)')
        return golfer_name

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(SiteServeException), reraise=True)
    def get_decimal_and_fractional_prices_in_ob_config_by_event(self, event):
        prices_formats = {'decimalPrice': None, 'fractionalPrice': None}
        markets = event['event']['children']
        children = None
        for market in markets:
            if SS_MARKET_LEVEL_DRILLDOWN_TAGS.LUCKY_DIP_DRILLDOWN in market['market']['drilldownTagNames']:
                children = market['market']['children'][0]['outcome']['children']
                break
        for child in children:
            if 'price' in child:
                prices_formats['decimalPrice'] = child['price']['priceDec']
                prices_formats['fractionalPrice'] = f"{child['price']['priceNum']}/{child['price']['priceDen']}"
        if len(prices_formats) == 0:
            raise SiteServeException('Decimal Price is not mentioned in Open Bet(OB)')
        return prices_formats

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(SiteServeException), reraise=True)
    def get_lucky_dip_market_description_by_event(self, event):
        """
        @param event: should pass event response from Site Server Call
        @return: dictionary of 'market_description' : description besides info icon under lucky dip,
                'display_name' : User Display Name under Lucky Dip, 'display_odds' : User Display Odds under Lucky Dip
        """
        result = {'market_description': None, 'display_name': None, 'display_odds': None}
        raw_description = None
        markets = event['event']['children']
        for market in markets:
            if SS_MARKET_LEVEL_DRILLDOWN_TAGS.LUCKY_DIP_DRILLDOWN in market['market']['drilldownTagNames']:
                raw_description = market['market']['name']
                break
        if not raw_description:
            raise SiteServeException('Random Golfer Name is Not Selected in Open Bet(OB)')
        raw_values = [value.strip().upper() for value in raw_description.split(',')]
        result['display_name'] = raw_values[0]
        result['market_description'] = raw_values[1]
        result['display_odds'] = raw_values[2]
        return result

    def create_lucky_dip_event(self, event_name: str = "AutoTESTLD", selection_name: str = "Random Golfer",
                               selection_number: int = 3, odds: str = "125/1"):
        selection_names = \
            [f'|{selection_name} {i + 1}|' for i in range(0, selection_number)]
        event = \
            self.ob_config.add_golf_event_to_golf_all_golf(
                max_bet=0.10,
                odds=odds,
                event_name=event_name,
                flag_FI_value="N",
                sort=self.lucky_dip_config["tournament_sort_code"],
                cashout=self.lucky_dip_config["event_level_cashout"],
                markets=self.lucky_dip_config["markets"],
                default_market=self.lucky_dip_config["default_market_config"]['market_name'],
                default_market_template_id=self.lucky_dip_config["default_market_config"]['market_template_id'],
                selections_names=selection_names, selections_number=selection_number,
                is_upcoming=True)
        self.__class__.created_event = event
        return self.created_event

    def settle_lucky_dip_event(self, selected_selection):
        if not self.created_event:
            raise SiteServeException(f"Event Is Not Created Please Check {self.create_lucky_dip_event.__name__}")
        event = self.created_event
        event_id = event.event_id
        self.ob_config.result_selection(
            selection_id=event.selection_ids['lucky_dip']['diplayed_selection'][selected_selection],
            market_id=event.all_markets_ids[event_id]['lucky_dip'], event_id=event_id, wait_for_update=True)
        self.ob_config.confirm_result(
            selection_id=event.selection_ids['lucky_dip']['diplayed_selection'][selected_selection],
            market_id=event.all_markets_ids[event_id]['lucky_dip'], event_id=event_id, wait_for_update=True)
        self.ob_config.settle_result(
            selection_id=event.selection_ids['lucky_dip']['diplayed_selection'][selected_selection],
            market_id=event.all_markets_ids[event_id]['lucky_dip'], event_id=event_id, wait_for_update=True)
