import random
import re
from collections import namedtuple

from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import external_keys
from crlat_siteserve_client.siteserve_client import query_builder
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string

import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


class BaseUKTote(BaseRacing):
    delete_events = False
    _ss_config = None
    start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
    end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'

    @classmethod
    def custom_setUp(cls, **kwargs):
        cls.get_ss_config()
        cls._check_uk_tote_events_presence()

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
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.INTERSECTS, 'UK')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_FLAG_CODES, OPERATORS.NOT_INTERSECTS, 'SP')) \
            .add_filter(external_keys(level=LEVELS.EVENT))
        # added NOT_INTERSECTS 'SP' above as it's misconfiguration and breaks page structure. BMA-42262 for reference

    @classmethod
    def _check_uk_tote_events_presence(cls):
        all_racing_events = cls.get_ss_config().ss_event_to_outcome_for_class(query_builder=cls.basic_active_events_filter())
        active_events_list = [event['event']['id'] for event in all_racing_events if 'event' in event.keys()]
        start, end = 0, 100
        uk_tote_events_available = False
        while len(active_events_list) > start:
            slice_ = active_events_list[start:end]
            active_events = ','.join(slice_)
            event_to_outcome_for_event = cls.get_ss_config().ss_event_to_outcome_for_event(
                event_id=active_events,
                query_builder=query_builder().add_filter(external_keys(level=LEVELS.EVENT))
            )

            uk_tote_events_available = next((True for record in reversed(event_to_outcome_for_event) if
                                             'externalKeys' in record.keys() and record['externalKeys']['externalKeyTypeCode'] == 'OBEvLinkTote'),
                                            False)
            if uk_tote_events_available:
                break
            start += 100
            end += 100

        if not uk_tote_events_available:
            raise SiteServeException('No UK Tote pools available')

    def get_uk_tote_event(self, raise_exceptions=True, **kwargs):
        event_params = namedtuple('uk_tote_event',
                                  ('event_id', 'uk_tote_event_id', 'event_typename', 'uk_tote_typename',
                                   'min_stake_per_line', 'stake_increment', 'min_total_stake', 'max_total_stake',
                                   'max_stake_per_line', 'market_id', 'event_time', 'selection_ids'))
        uk_tote_event = event_params(event_id=None, uk_tote_event_id=None, event_typename=None, uk_tote_typename=None,
                                     min_stake_per_line=None, stake_increment=None, min_total_stake=None,
                                     max_total_stake=None, max_stake_per_line=None, market_id=None, event_time=None,
                                     selection_ids=None)
        event_filter = self.ss_query_builder.add_filter(external_keys(level=LEVELS.EVENT))
        pool_filters = self.ss_query_builder.add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE, OPERATORS.EQUALS, 'true'))

        all_racing_events = self.ss_req.ss_event_to_outcome_for_class(query_builder=self.basic_active_events_filter())
        events_list = [event for event in all_racing_events if 'event' in event.keys()]

        active_events_list = []
        for event in events_list:
            outcomes_active = True
            if not event['event'].get('children'):
                continue
            for market in event['event']['children']:
                if not market['market'].get('children'):
                    continue
                for outcome in market['market']['children']:
                    if outcome['outcome']['outcomeStatusCode'] != 'A' and 'N/R' not in outcome['outcome']['name']:
                        outcomes_active = False
                        break
            if outcomes_active:
                active_events_list.append(event)

        for k, v in kwargs.items():
            if 'uk_tote' in k:
                pool_filters.add_filter(
                    simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, vec.siteserve.POOLS_TYPES_CODES.get(k)))

        random.shuffle(active_events_list)

        for event in active_events_list:
            racing_event_id = event['event']['id']
            market_id = event['event']['children'][0]['market']['id']
            ss_event = self.ss_req.ss_event_to_outcome_for_event(
                event_id=racing_event_id,
                query_builder=event_filter,
                raise_exceptions=False)
            for record in reversed(ss_event):
                if 'externalKeys' in record.keys() and record['externalKeys']['externalKeyTypeCode'] == 'OBEvLinkTote':
                    mappings = record['externalKeys']['mappings']
                    uk_tote_event_id = mappings.replace(racing_event_id, '').replace('event', '').replace(',', '')
                    ss_uk_event_pools = self.ss_req.ss_pool_for_event(event_id=uk_tote_event_id, query_builder=pool_filters)
                    if ss_uk_event_pools:
                        pool = ss_uk_event_pools[0]['pool']
                        min_total_stake = float(pool['minTotalStake'])
                        min_stake_per_line = float(pool['minStakePerLine'])
                        stake_increment = float(pool['stakeIncrementFactor'])
                        max_total_stake = float(pool['maxTotalStake'])
                        max_stake_per_line = float(pool['maxStakePerLine'])
                        event_typename = ss_event[0]['event']['typeName'].strip('|')
                        event_time = (re.search(r'\d*:\d*', ss_event[0]['event']['name'])).group()
                        selection_ids = [i['outcome']['id'] for i in
                                         ss_event[0]['event']['children'][0]['market']['children']]
                        ss_uk_tote_event = self.ss_req.ss_event_to_outcome_for_event(
                            event_id=uk_tote_event_id,
                            raise_exceptions=False
                        )
                        if not ss_uk_tote_event:
                            continue
                        uk_tote_typename = ss_uk_tote_event[0]['event']['typeName']
                        uk_tote_event = event_params(event_id=racing_event_id, uk_tote_event_id=uk_tote_event_id,
                                                     event_typename=event_typename, uk_tote_typename=uk_tote_typename,
                                                     min_total_stake=min_total_stake, min_stake_per_line=min_stake_per_line,
                                                     stake_increment=stake_increment, max_total_stake=max_total_stake,
                                                     max_stake_per_line=max_stake_per_line, market_id=market_id,
                                                     event_time=event_time, selection_ids=selection_ids)
                        return uk_tote_event
        if uk_tote_event.event_id is None and raise_exceptions:
            parameters_message = f' with parameters {kwargs}' if kwargs else ''
            raise SiteServeException(f'No required UK Tote pools available{parameters_message}')
        return uk_tote_event

    def get_single_leg_outcomes(self, event_id: str, tab_name: str) -> list:
        """
        Method to get list of Exacta or Trifecta outcomes for UK Tote racing event

        :param event_id: ID of UK Tote event
        :param tab_name: Name of the subtab of Totepool tab, Exacta or Trifecta
        :return: list[(str, SingleUKToteOutcome), (str, SingleUKToteOutcome) ...]
                 list[(outcome name, SingleUKToteOutcome object), (outcome name, SingleUKToteOutcome object) ...]
        """
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        section_name, section = list(sections.items())[0]
        tab_opened = section.grouping_buttons.click_button(tab_name)
        self.assertTrue(tab_opened, msg=f'{tab_name} tab is not opened')

        outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(outcomes, msg=f'No outcomes found in {section_name} selection')

        return outcomes

    def place_multiple_legs_bet(self, event_id: str, tab_name: str, unit_stake: float) -> dict:
        """
        Method to place bet on multiple legs event. One selection per each leg

        :param event_id: Id of event to place bet
        :param tab_name: Name of the sub tab of Totepool tab, Quadpot, Placepot or Jackpot
        :param unit_stake: Amount of unit stake
        :return: dict {selected_outcomes: [Outcome name 1, Outcome name 2, ...],
                       races_titles: [Title of Leg1, Title of Leg2, ... ]}
        """
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        section_name, section = list(sections.items())[0]
        tab_opened = section.grouping_buttons.click_button(tab_name)
        self.assertTrue(tab_opened, msg='"%s" tab is not opened' % vec.uk_tote.UK_TOTE_TABS.quadpot)

        pool = section.pool
        pool_legs = pool.grouping_buttons.items_as_ordered_dict
        self.assertTrue(pool_legs, msg='There are no available pool legs')
        selected_outcomes = []
        races = []

        for pool_leg_name, pool_leg in pool_legs.items():
            pool.grouping_buttons.click_button(button_name=pool_leg_name)
            races.append(pool.race_title)

            outcomes = pool.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcomes found for pool leg: "%s"' % pool_leg_name)

            selected_outcome = list(outcomes.items())[0]
            outcome_name, outcome = selected_outcome
            selected_outcomes.append(outcome_name)
            outcome.select()

        section.bet_builder.summary.input.value = unit_stake
        section.bet_builder.summary.add_to_betslip_button.click()

        return {'selected_outcomes': selected_outcomes, 'races_titles': races}
