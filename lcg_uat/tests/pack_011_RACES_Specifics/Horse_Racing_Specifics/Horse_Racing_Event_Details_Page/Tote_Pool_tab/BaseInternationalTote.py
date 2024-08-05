from collections import namedtuple
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import external_keys
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec

from voltron.utils.exceptions.siteserve_exception import SiteServeException


class BaseInternationalTote(BaseRacing):
    delete_events = False
    _ss_config = None
    start_date = f'{get_date_time_as_string(days=0, hours=1, time_format="%Y-%m-%dT%H:%M:%S.000Z")}'
    end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'

    @classmethod
    def get_ss_config(cls):
        if not cls._ss_config:
            ob_config = cls.get_ob_config()
            cls._ss_config = SiteServeRequests(env=tests.settings.backend_env,
                                               brand=cls.brand,
                                               category_id=ob_config.backend.ti.tote.category_id,
                                               class_id=ob_config.backend.ti.tote.horse_intl_thoroughbred_pools.class_id
                                               )
        return cls._ss_config

    @classmethod
    def custom_setUp(cls, **kwargs):
        cls.get_ss_config()

    @classmethod
    def basic_active_events_filter(cls):
        return query_builder() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.NAME, OPERATORS.NOT_EQUALS, '%7Cnull%7C')) \
            .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL, cls.start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN, cls.end_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      cls.start_date_minus)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(exists_filter(LEVELS.EVENT,
                                      simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS,
                                                    'A'))) \
            .add_filter(external_keys(level=LEVELS.EVENT))

    def get_int_tote_event(self, raise_exceptions=True, **kwargs):
        event_params = namedtuple('int_tote_event',
                                  ('event_id', 'int_tote_event_id', 'event_typename', 'int_tote_typename',
                                   'min_stake_per_line', 'stake_increment', 'min_total_stake', 'max_total_stake',
                                   'max_stake_per_line', 'market_id', 'currency_code'))
        int_tote_event = event_params(event_id=None, int_tote_event_id=None, event_typename=None,
                                      int_tote_typename=None,
                                      min_stake_per_line=None, stake_increment=None, min_total_stake=None,
                                      max_total_stake=None, max_stake_per_line=None, market_id=None, currency_code=None)
        event_filter = self.basic_active_events_filter()

        pool_filters = self.ss_query_builder.add_filter(
            simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE, OPERATORS.EQUALS, 'true'))
        outcome_filter = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(exists_filter(LEVELS.EVENT,
                                      simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS,
                                                    'A')))\
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')))

        for k, v in kwargs.items():
            if 'int_tote' in k:
                pool_filters.add_filter(
                    simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, vec.siteserve.INT_POOLS_TYPES_CODES.get(k)))

        resp = self.ss_req.ss_event_to_market_for_class(query_builder=event_filter, raise_exceptions=False)
        if not resp and raise_exceptions:
            parameters_message = f' with parameters {kwargs}' if kwargs else ''
            raise SiteServeException(f'No required International Tote pools available{parameters_message}')

        external_mappings = [event for event in resp if 'externalKeys' in event.keys()]
        # active_events_list = [event for event in resp if 'event' in event.keys()]

        # mappings: "9568204,9562077,event,9568202,9562075,event,9568203,9562076,event,"
        for record in reversed(external_mappings):
            if 'externalKeys' in record.keys() and record['externalKeys']['externalKeyTypeCode'] == 'OBEvLinkNonTote':
                mappings = record['externalKeys']['mappings']
                mappings_split = mappings.split(',event,')
                for mapping in mappings_split:
                    events_ids = mapping.split(',')
                    ob_event_id = events_ids[1]
                    int_tote_event_id = events_ids[0]
                    ss_int_event_pools = self.ss_req.ss_pool_for_event(event_id=int_tote_event_id,
                                                                       query_builder=pool_filters)
                    if ss_int_event_pools:
                        pool = ss_int_event_pools[0]['pool']
                        min_total_stake = float(pool['minTotalStake'])
                        min_stake_per_line = float(pool['minStakePerLine'])
                        stake_increment = float(pool['stakeIncrementFactor'])
                        max_total_stake = float(pool['maxTotalStake'])
                        max_stake_per_line = float(pool['maxStakePerLine'])
                        pool_currency = pool['currencyCode']

                        ss_int_tote_event = self.ss_req.ss_event_to_outcome_for_event(
                            event_id=int_tote_event_id,
                            raise_exceptions=False
                        )
                        if not ss_int_tote_event:
                            continue
                        int_tote_typename = ss_int_tote_event[0]['event']['typeName']
                        ob_event_typename, ob_market_id = None, None

                        ss_ob_event = self.ss_req.ss_event_to_outcome_for_event(
                            event_id=ob_event_id,
                            query_builder=outcome_filter,
                            raise_exceptions=False
                        )
                        if not ss_ob_event:
                            continue

                        ob_event_typename = ss_ob_event[0]['event']['typeName'].strip('|')
                        ob_market_id = ss_ob_event[0]['event']['children'][0]['market']['id']
                        int_tote_event = event_params(event_id=ob_event_id, int_tote_event_id=int_tote_event_id,
                                                      event_typename=ob_event_typename,
                                                      int_tote_typename=int_tote_typename,
                                                      min_total_stake=min_total_stake,
                                                      min_stake_per_line=min_stake_per_line,
                                                      stake_increment=stake_increment, max_total_stake=max_total_stake,
                                                      max_stake_per_line=max_stake_per_line, market_id=ob_market_id,
                                                      currency_code=pool_currency)
                        return int_tote_event

        if int_tote_event.event_id is None and raise_exceptions:
            parameters_message = f' with parameters {kwargs}' if kwargs else ''
            raise SiteServeException(f'No required International Tote pools available{parameters_message}')
        return int_tote_event

    def get_single_leg_outcomes(self, event_id: (int, str), tab_name: str) -> list:
        """
        :param event_id: id of related event with Tote pools
        :param tab_name: pool type
        :return: list of outcomes for given International Tote pool
        """
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')

        tab_content = self.site.racing_event_details.tab_content
        tab_opened = tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg=f'"{vec.uk_tote.TOTEPOOL}" tab is not opened')
        self.__class__.event_off_time = tab_content.event_off_times_list.selected_item
        sections = tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        win_tab_opened = section.grouping_buttons.click_button(tab_name)
        self.assertTrue(win_tab_opened, msg=f'"{tab_name}" tab is not opened')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.pool.items_as_ordered_dict
        self.assertTrue(all(outcomes), msg='No outcomes found')
        return [(outcome_name, outcome) for (outcome_name, outcome) in outcomes.items() if outcome.is_enabled()]
