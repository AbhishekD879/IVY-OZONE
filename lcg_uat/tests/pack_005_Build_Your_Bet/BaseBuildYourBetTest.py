import random
import time
from collections import namedtuple
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
from typing import NamedTuple

from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_ob_client.utils.date_time import get_date_time_object
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from dateutil.parser import parse
from selenium.common.exceptions import StaleElementReferenceException
from tzlocal import get_localzone

import tests
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.device.device_manager import DeviceManager
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import do_request
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


class BaseBanachTest(BaseSportTest):
    selection = None
    my_bets_single_build_your_bet_title = vec.yourcall.DASHBOARD_TITLE
    initial_counter = 0
    proxy_admin_hostname = tests.settings.proxy_admin_banach
    byb_hostname = tests.settings.banach_api_hostname
    banach_events = tests.settings.banach_events_endpoint
    banach_leagues_upcoming = tests.settings.banach_leagues_upcoming_endpoint
    banach_leagues = tests.settings.banach_leagues_endpoint
    config_endpoint = tests.settings.banach_config_endpoint
    set_event_id_endpoint = tests.settings.banach_set_event_id_endpoint
    banach_players_endpoint = tests.settings.banach_players_endpoint
    banach_selections_endpoint = tests.settings.banach_selections_endpoint
    banach_statistics_endpoint = tests.settings.banach_statistics_endpoint
    banach_statistic_values_endpoint = tests.settings.banach_statistic_values_endpoint
    banach_markets_grouped_endpoint = tests.settings.banach_markets_grouped_endpoint
    byb_on_homepage = False
    response_50011 = '50011'
    response_51101 = '51101'
    response_50001 = '50001'
    response_51001 = '51001'
    is_bet_builder_tab_created_manually = False

    proxy = tests.settings.banach_socks_proxy_hostname

    @property
    def headers(self):
        return {'origin': f'https://{tests.HOSTNAME}',
                'user-agent': DeviceManager.supported_devices.get(self.device_name, {}).get('user-agent','Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation'),
                'referer': f'https://{tests.HOSTNAME}',
                'accept': 'application/json, text/plain, */*',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'authority': tests.settings.banach_api_hostname,
                'accept-language': 'en-US,en;q=0.9'
                }

    @classmethod
    def custom_setUp(cls, **kwargs):
        cms_config = cls.get_cms_config()
        system_config = cls.get_initial_data_system_configuration()
        if not system_config.get('YourCallIconsAndTabs', {}).get('enableTab'):
            raise CmsClientException('Build Your Bet is disabled in CMS. Please check the "enableTab" parameter of "YourCallIconsAndTabs" in CMS system config..')
        if cls.byb_on_homepage:
            byb_tab_cms = next(
                (tab.get('title').upper() for i, tab in enumerate(cms_config.module_ribbon_tabs.visible_tabs_data)
                 if tab.get('directiveName') == 'BuildYourBet' and tab.get('title').upper() == vec.yourcall.DASHBOARD_TITLE.upper()), None)
            if byb_tab_cms is None:
                cls._logger.info(f'"{vec.yourcall.DASHBOARD_TITLE}" is unavailable. Creating the "{vec.yourcall.DASHBOARD_TITLE}"......')
                internal_id = 'tab-build-your-bet' if cls.brand == 'bma' else 'tab-bet-builder'
                cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id=internal_id, title=vec.yourcall.DASHBOARD_TITLE)
                cms_config.module_ribbon_tabs._created_tabs.pop()
                cls.is_bet_builder_tab_created_manually = True

    @property
    def proxies(self):
        return {'https': self.proxy.replace('socks5', 'socks5h')} \
            if self.proxy \
            else None

    def get_event_id_from_mock(self):
        url = self.proxy_admin_hostname + self.config_endpoint
        return do_request(url=url, method='GET', proxies=self.proxies)['event_id']

    def create_ob_event_for_mock(self, **kwargs):
        """
        Can be used only when proxy is enabled, i.e proxy variable is not set to None
        """
        self.__class__.team1, self.__class__.team2 = kwargs.get('team1', 'Test team 1'), kwargs.get('team2', 'Test team 2')
        create_event = None
        event_id = self.get_event_id_from_mock()

        if event_id:  # from mock service
            result = wait_for_result(lambda: self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, raise_exceptions=False),
                                     name='Waiting for event to be available on SiteServe',
                                     poll_interval=1,
                                     timeout=10)
            result = result[0] if result else {}
            if not result:
                self._logger.debug(f'______ Event {event_id} not found in SS response {result}')
                create_event = True
            elif 'event' not in result.keys() or result['event']['id'] != event_id:
                self._logger.debug(f'______ Event {event_id} not found in SS response {result}')
                create_event = True
            else:
                if parse(result['event']['startTime'], yearfirst=True).day < datetime.utcnow().day:
                    self._logger.debug('______ Event start time is not today, need to create new event')
                    create_event = True
                elif result['event']['eventStatusCode'] == 'S':
                    self._logger.debug('______ Event is not active, need to create new event')
                    create_event = True
                elif 'children' not in result['event'] or result['event']['children'][0]['market']['marketStatusCode'] == 'S' \
                        or result['event']['children'][0]['market']['isActive'] != 'true':
                    self._logger.debug('______ Market is not active, need to create new event')
                    create_event = True
        else:
            self._logger.debug('______ Event id is not received from mock, need to create new event')
            create_event = True

        if create_event:
            self._logger.debug(f'______ Suspending old OB event {event_id}')
            self.ob_config.change_event_state(event_id=event_id) if event_id else \
                self._logger.debug('______ Skipping event suspension, event id not found')
            self._logger.debug('______ Creating new OB event to use in mock')
            event_params = self.ob_config.add_football_event_to_england_premier_league(team1=self.team1,
                                                                                       team2=self.team2)
            new_event_id = event_params.event_id
            self.ob_config.CREATED_EVENTS.remove(new_event_id)
            self._logger.debug('______ Updating event id in mock')
            url = self.proxy_admin_hostname + self.set_event_id_endpoint
            self._logger.debug(f'______ New event id {new_event_id}')
            do_request(url=url, method='POST', data=new_event_id, proxies=self.proxies, load_response=False)
        else:
            self._logger.info(f'______ Using event id {event_id} from mock')
            new_event_id = event_id
        return new_event_id

    def get_ob_event_with_byb_market(self, market_name: str = None, **kwargs):
        """
        Can be used only when proxy is disabled, i.e. proxy variable is set to None
        """
        five_a_side = kwargs.get('five_a_side')
        url = f'{self.byb_hostname}{self.banach_events}'
        url_markets_grouped = f'{self.byb_hostname}{self.banach_markets_grouped_endpoint}'
        event_id = None
        r = do_request(method='GET', url=url, headers=self.headers, proxies=self.proxies)
        cms_your_call_leagues = self.cms_config.get_your_call_leagues()
        type_ids_of_leagues_with_yc_available = [str(league['typeId']) for league in cms_your_call_leagues if league.get('enabled')]
        banach_events_data = r.get('data', [])
        self._logger.debug(f'*** Found {len(banach_events_data)} events from Banach')
        random.shuffle(banach_events_data)

        for i, event in enumerate(banach_events_data):
            self._logger.debug(f'*** Checking event #{i}/{len(banach_events_data)}')
            if five_a_side is False and event.get('hasPlayerProps') is True:
                continue
            if five_a_side is True and not event.get('hasPlayerProps'):
                continue
            ob_event_id = event['obEventId']
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=ob_event_id, raise_exceptions=False)
            if not event_resp or not event_resp[0].get('event', {}).get('children', []):
                continue
            banach_markets = do_request(method='GET', headers=self.headers, url=url_markets_grouped, proxies=self.proxies, params=[('obEventId', ob_event_id)])
            if not banach_markets['data']:
                continue
            if market_name:
                if market_name == 'Player Bets':
                    # player bets market is not present in markets-grouped response
                    url_players = f'{self.byb_hostname}{self.banach_players_endpoint}'
                    params_players = (
                        ('obEventId', ob_event_id),
                    )
                    r_players = do_request(method='GET', headers=self.headers, url=url_players, proxies=self.proxies, params=params_players)
                    if isinstance(r_players, dict) and r_players.get('data'):
                        players = [r_players.get('data')[0]]
                        # trying to check that at least one player has statistic
                        for player in players:
                            player_id = player.get('id')
                            url_statistics = f'{self.byb_hostname}{self.banach_statistics_endpoint}'
                            params_statistics = (
                                ('obEventId', ob_event_id),
                                ('playerId', player_id)
                            )
                            r_statistics = do_request(method='GET', headers=self.headers, url=url_statistics, proxies=self.proxies, params=params_statistics)
                            if isinstance(r_statistics, dict) and r_statistics.get('data'):
                                break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    for market in banach_markets['data']:
                        if market['marketGroupName'] == market_name:
                            break
                        else:
                            continue
                    else:
                        continue
            event_resp = event_resp[0]
            if 'event' in event_resp:
                ob_event = event_resp['event']
                type_id = ob_event['typeId']
                if type_id not in type_ids_of_leagues_with_yc_available:
                    continue
                is_finished, is_resulted, is_started, is_live_now = \
                    ob_event.get('isFinished', None), ob_event.get('isResulted', None), ob_event.get('isStarted', None), \
                    ob_event.get('isLiveNowEvent', None)
                if any((status == 'true' for status in (is_finished, is_resulted, is_started, is_live_now))):
                    continue
                is_active, event_status_code = ob_event.get('isActive'), ob_event.get('eventStatusCode')
                if is_active != 'true' or event_status_code != 'A':
                    continue
                event_id = ob_event_id
                event_name = normalize_name(ob_event.get('name', ''))
                self.__class__.team1 = event.get('homeTeam').get('title')
                self.__class__.team2 = event.get('visitingTeam').get('title')
                self._logger.info(f'*** Found event "{event_name}" id "{event_id}" with Banach markets available on SiteServe')
                break
        if not event_id:
            raise SiteServeException('Cannot found OB event with Banach markets available')
        return event_id

    def get_banach_leagues(self) -> dict:
        """
        Gets leagues from buildyourbet
        https://buildyourbet-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/v1/leagues
        :return: list of Banach leagues
        """
        is_dst = time.localtime().tm_isdst
        url = f'{self.byb_hostname}{self.banach_leagues}'
        params = [('days', 6), ('tz', (2 + is_dst) if tests.location not in ['AWS', 'AWS_GRID'] else 0)]
        r = do_request(method='GET', headers=self.headers, url=url, proxies=self.proxies, params=params)
        data = r.get('data', [])
        leagues_names = [item['title'].strip('|').upper() for item in data]
        leagues_ids = [item['obTypeId'] for item in data]
        leagues_data = dict(zip(leagues_names, leagues_ids))
        return leagues_data

    def get_upcoming_leagues(self) -> dict:
        """
        Gets upcoming leagues data from buildyourbet
        https://buildyourbet-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=6&tz=2
        :return: dict today/upcoming leagues information
        """
        is_dst = time.localtime().tm_isdst
        url = f'{self.byb_hostname}{self.banach_leagues_upcoming}'
        params = [
            ('days', 6),
            ('tz', is_dst if tests.location not in tests.settings.utc_locations else 0)
        ]
        r = do_request(method='GET', headers=self.headers, url=url, proxies=self.proxies, params=params)
        return r.get('data', [])

    def check_event_is_active(self, event_id: (str, int)) -> bool:
        """
        Checks if event with given id is active (event status code is active, market status code is active, outcomes status codes are active
        :param event_id: id of event
        :return: True or False depending if event is active or not
        """
        query = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A'))\
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.MARKET_STATUS_CODE, OPERATORS.EQUALS, 'A')))\
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.OUTCOME, ATTRIBUTES.OUTCOME_STATUS_CODE, OPERATORS.EQUALS, 'A')))

        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=query, raise_exceptions=False)
        return True if resp else False

    def check_byb_leagues_presence(self) -> namedtuple:
        """
        Checks if today/upcoming leagues should be displayed depending on events status in these leagues
        :return: namedtuple with keys 'today', 'upcoming' that have True/False values depending on events statuses
        """
        byb_leagues_from_banach = self.get_upcoming_leagues()
        today_banach_leagues, upcoming_banach_leagues = byb_leagues_from_banach.get(
            'today', []), byb_leagues_from_banach.get('upcoming', [])
        today_events, upcoming_events = False, False
        for league in today_banach_leagues:
            expected_events_response = self.get_events_for_league(league_id=league['obTypeId'], day_from=-1,
                                                                  day_to=1)
            today_events = any(self.check_event_is_active(event_id=event['obEventId']) for event in expected_events_response)
            if today_events:
                break

        for league in upcoming_banach_leagues:
            expected_events_response = self.get_events_for_league(league_id=league['obTypeId'], day_from=0, day_to=5)
            upcoming_events = any(self.check_event_is_active(event_id=event['obEventId']) for event in expected_events_response)
            if upcoming_events:
                break

        isPresent = NamedTuple('today_upcoming_presence', [('today', bool), ('upcoming', bool)])
        params = isPresent(today_events, upcoming_events)
        return params

    def get_mapped_leagues(self, date_range: str) -> dict:
        """
        Gets Banach leagues type ids and names that have mappings in CMS
        :param date_range: either today or upcoming
        :return: dictionary of leagues type ids and names
        """
        mapped_leagues = {}
        cms_your_call_leagues = self.cms_config.get_your_call_leagues()

        leagues_from_banach = self.get_upcoming_leagues()
        leagues = leagues_from_banach.get(date_range, [])
        for cms_league in cms_your_call_leagues:
            if not cms_league.get('enabled'):
                continue
            type_id = cms_league['typeId']
            league_name = None

            for league in leagues:
                if str(league['obTypeId']) == str(cms_league['typeId']):
                    resp = self.ss_req.ss_class_to_sub_type_for_type(type_ids=type_id,
                                                                     query_builder=self.ss_query_builder,
                                                                     raise_exceptions=False)
                    if not resp:
                        continue
                    for ob_type in resp[0]['class']['children']:
                        if ob_type['type']['id'] == str(league['obTypeId']):
                            league_name = ob_type['type']['name'].replace('|', '')
            if not league_name:
                continue
            # This is workaround if there are two leagues with the same type id in CMS
            # Dev's code take last one, we should do the same
            mapped_leagues.pop(type_id, None)
            mapped_leagues[type_id] = league_name
        return mapped_leagues

    def get_events_for_league(self, league_id: (str, int) = None, day_from: int = 0, day_to: int = 5) -> list:
        """
        Gets events that belong to specific league (by league id which is OB type id)
        https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/
        events?leagueIds=442&dateFrom=2018-11-21T22:00:00.000Z&dateTo=2018-11-26T22:00:00.000Z
        :param league_id: OB league type id
        :param day_from: day number starting from 0 (today)
        :param day_to: day number 1 (tomorrow)
        :return: list of events objects
        """
        self._logger.info(f'*** Found timezone: "{get_localzone()}"')
        timezone = 'Europe/Kiev'
        time_delta = timedelta(days=1) - get_date_time_object(tz_region=str(timezone)).utcoffset()
        start_date = get_date_time_as_string(time_format=f'%Y-%m-%dT{time_delta}.000Z', days=day_from)
        base_date = get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S", days=day_to)
        end_date = f'{get_date_time_as_string(datetime.strptime(base_date, "%Y-%m-%dT%H:%M:%S") + time_delta, time_format="%Y-%m-%dT%H")}:00:00.000Z'
        url = f'{self.byb_hostname}{self.banach_events}'
        params = [
            ('leagueIds', league_id),
            ('dateFrom', start_date),
            ('dateTo', end_date)
        ]
        r = do_request(method='GET', headers=self.headers, url=url, proxies=self.proxies, params=params)
        return r.get('data', [])

    def get_players_for_event(self, event_id: (int, str)) -> namedtuple:
        """
        Gets players for event
        :param event_id: id of event
        :return: namedtuple where 1st item is list of players, 2nd - players info dict as it comes from BYB
        """
        url = '%s%s' % (self.byb_hostname, self.banach_players_endpoint)
        params = (
            ('obEventId', event_id),
        )
        r = do_request(method='GET', headers=self.headers, url=url, proxies=self.proxies, params=params)
        if not isinstance(r, dict) or not r.get('data'):
            raise SiteServeException(f'No testing data found, request for getting players for event: '
                                     f'{event_id} failed with error: "{r}", url "{url}"')
        player_names = [player.get('name') for player in r['data'] if player.get('name')]
        self._logger.info(f'*** Found players: "{player_names}"')
        self.assertTrue(player_names, msg=f'Cannot find players for OB event: "{event_id}"')
        Params = namedtuple('player_params', ['as_list_of_names', 'as_json_resp'])
        player_params = Params(player_names, r)
        return player_params

    def get_statistics(self, event_id: (str, int), **kwargs) -> namedtuple:
        """
        Get statistics for given player
        :param event_id: id of event to which player belongs
        :return: namedtuple where 1st item is statistics names, 2nd - statistics info dict as it comes from BYB
        """
        url = f'{self.byb_hostname}{self.banach_statistics_endpoint}'
        playerId = kwargs.get('byb_player_id', 1)
        params = (
            ('obEventId', event_id),
            ('playerId', playerId)
        )
        r = do_request(method='GET', headers=self.headers, url=url, proxies=self.proxies, params=params)
        if not isinstance(r, dict) or not r.get('data'):
            raise SiteServeException(f'No testing data found, request for getting statistics for event: '
                                     f'{event_id} and player id {playerId} failed with error: "{r}", url "{url}"')
        statistics_names = [statistic.get('title') for statistic in r['data'] if statistic.get('title')]
        self._logger.info(f'*** Found statistics: "{statistics_names}"')
        self.assertTrue(statistics_names, msg=f'Cannot find statistics for OB event: "{event_id}"')
        Params = namedtuple('statistics_params', ['as_list_of_names', 'as_json_resp'])
        stat_params = Params(statistics_names, r)
        return stat_params

    def get_statistic_values(self, event_id: (str, int), **kwargs) -> namedtuple:
        """
        Gets statistics value range for statistic
        :param event_id: id of event
        :return: named tuple where 1st item is list of statistic values, 2nd - values range info dict as it comes from BYB: min, max and average statistic values
        """
        url = '%s%s' % (self.byb_hostname, self.banach_statistic_values_endpoint)
        player_id = kwargs.get('byb_player_id', 1)
        stat_id = kwargs.get('byb_statistic_id', 6)
        params = (
            ('obEventId', event_id),
            ('playerId', player_id),
            ('statId', stat_id),
        )
        r = do_request(method='GET', headers=self.headers, url=url, proxies=self.proxies, params=params)
        if not isinstance(r, dict) or not r.get('data'):
            raise SiteServeException(f'No testing data found, request for getting statistics for event: '
                                     f'{event_id} and player id {player_id} failed with error: "{r}", url "{url}"')
        values = r['data']
        import math
        values['average'] = math.ceil(values.get('average')) if values.get('average', 0) else 0
        start, end = math.ceil(values.get('minValue', 0)), math.ceil(values.get('maxValue', 0))
        values_list = [str(i) for i in range(start, end + 1)]
        self._logger.info(f'*** Found statistic value range: "{values_list}"')
        self.assertTrue(values_list, msg=f'Cannot find value range for OB event: "{event_id}"')
        Params = namedtuple('values_params', ['as_list_of_names', 'as_json_resp'])
        values_params = Params(values_list, values)
        return values_params

    def get_byb_module_accordions(self, module_name='BUILD YOUR BET', switcher_name=None) -> OrderedDict:
        """
        Gets BYB accordions on home page for given grouping
        :param switcher_name: today or upcoming, if not specified then assuming today
        :return: dictionary where keys are accordion names and values are BYBEventGroup object
        """
        grouping = switcher_name if switcher_name else vec.yourcall.TODAY
        byb_tab_content = self.site.home.get_module_content(module_name=module_name)
        self.assertTrue(byb_tab_content.has_grouping_buttons,
                        msg='Build Your Bet tab does not have Today/Upcoming switchers')
        byb_tab_content.grouping_buttons.click_button(grouping)
        byb_tab_accordions = byb_tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(byb_tab_accordions, msg=f'No accordions found for "{grouping}"')
        return byb_tab_accordions

    def get_market(self, market_name):
        markets = self.site.sport_event_details.tab_content.accordions_list.get_items(name=market_name)
        self.assertTrue(markets, msg=f'Cannot find markets on page')
        req_market = next(
            (avl_market_name for avl_market_name in markets if avl_market_name.upper() == market_name.upper()), None)
        market = markets.get(req_market)
        self.assertTrue(market, msg=f'Cannot find market "{market_name}"')
        market.expand()
        markets = wait_for_result(
            lambda: self.site.sport_event_details.tab_content.accordions_list.get_items(name=market_name), timeout=30)
        market = markets.get(req_market)
        return market

    def add_byb_selection_to_dashboard(self, market_name: str, switcher_name: str = None, **kwargs) -> list:
        """
        :param market_name: Name of market
        :param switcher_name: Name of switcher button (only for markets with switchers)
        :param kwargs: Prioritized market selection parameters:
          - add selection outcome by name  if 'selection_name' specified;
          - add selection outcome by index if 'selection_index' specified;
          - add specified selections count is 'count' specified;
          - add all market selections if **kwargs empty
        :return: selection_names: List of added selections names
        """
        market = self.get_market(market_name=market_name)
        if switcher_name:
            result = market.grouping_buttons.click_button(switcher_name)
            self.assertTrue(result, msg=f'Switcher "{switcher_name}" is not active for "{market_name}"')
        selection_names = market.set_market_selection(**kwargs)
        self.assertTrue(selection_names, msg='No selection from "%s" was added to Dashboard' % market_name)
        self.site.sport_event_details.tab_content.wait_for_dashboard_panel()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.__class__.initial_counter += 1
        return selection_names

    def get_byb_dashboard_outcomes(self) -> OrderedDict:
        """
        On EDP, having Build Your Bet tab active and outcomes added to dashboard, gets them
        :return: OrderedDict with outcomes, where key is outcome name, value - BYBListItem object
        """
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        dashboard_outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(dashboard_outcomes, msg=f'No outcomes found on BYB Dashboard: "{dashboard_outcomes}"')
        return dashboard_outcomes

    def get_byb_dashboard_outcome(self, name: str):
        """
        Gets BYB Dashboard outcome by name
        :param name: name of outcome as it is displayed on BYB Dashboard, e.g.: Match Betting 90 mins TEST TEAM 1
        :return: BYBListItem object
        """
        dashboard_outcomes = self.get_byb_dashboard_outcomes()
        outcome = dashboard_outcomes.get(name)
        self.assertTrue(outcome,
                        msg=f'{name} was not found in list of dashboard outcomes "{dashboard_outcomes.keys()}"')
        return outcome

    def add_player_bet_selection_to_dashboard(self, **kwargs):
        """
        Adding player bet selections to dashboard
        :param player_index: int starting from 1
        :param player_name: string
        :param statistic_name: string
        :param statistic_value: string
        :return: named tuple with selection information
        """
        self.site.sport_event_details.tab_content.accordions_list.wait_item_appears(self.expected_market_sections.player_bets)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Market list is not found')
        player_bet_market = markets_list.get(self.expected_market_sections.player_bets)
        self.assertTrue(player_bet_market, msg='PLAYER BETS section is not found')
        player_bet_market.expand()
        self.assertTrue(player_bet_market.is_expanded(),
                        msg=f'Market "{self.expected_market_sections.player_bets}" is not expanded')
        player_bet_info = player_bet_market.set_player_bet_selection(**kwargs)
        self.assertTrue(player_bet_market.has_add_to_bet_button(), msg='ADD TO BET button does not exist')
        player_bet_market.add_to_bet_button.click()
        return player_bet_info

    def remove_all_selections_from_dashboard(self):
        selections = self.site.sport_event_details.tab_content.dashboard_panel.outcomes_section.items_as_ordered_dict.items()
        self.assertTrue(selections, msg='No selections found')
        for i in range(0, len(selections)):
            try:
                dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
                selection_name, selection = list(dashboard_panel.outcomes_section.items_as_ordered_dict.items())[-1]
            except (VoltronException, StaleElementReferenceException):
                dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
                selection_name, selection = list(dashboard_panel.outcomes_section.items_as_ordered_dict.items())[-1]
            selection.remove_button.click()
            self.device.driver.implicitly_wait(0.5)
            if (i + 1 != len(selections)) and self.site.sport_event_details.tab_content.wait_for_dashboard_panel(timeout=2):
                self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
                self.__class__.initial_counter -= 1
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet dashboard is still shown')
        self.device.driver.implicitly_wait(0)
