from collections import namedtuple, OrderedDict
import logging
import re
from random import randint
from time import sleep
import typing
import datetime
import xmltodict, json
from urllib.parse import urljoin
from crlat_siteserve_client.siteserve_client import query_builder, translation_lang
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
import lxml.html as html
from crlat_ob_client import LOGGER_NAME
from crlat_ob_client.create_event import CreateSportEvent, Coupon, CreateRacingEvent
from crlat_ob_client.freebet import Freebet
from crlat_ob_client.freeride import Freeride
from crlat_ob_client.odds_boost import OddsBoost
from crlat_ob_client.login import OBLogin
from crlat_ob_client.markets.win_draw_win_market import WinDrawWinMarket
from crlat_ob_client.markets.win_win_market import WinWinMarket
from crlat_ob_client.utils.exceptions import OBException
from crlat_ob_client.utils.helpers import do_request, generate_name
from crlat_ob_client.utils.waiters import wait_for_result
from faker import Faker


_logger = logging.getLogger(LOGGER_NAME)


class OBConfig(OBLogin):
    backend = None

    def __init__(self, env, brand, *args, **kwargs):
        super(OBConfig, self).__init__(env, brand, args, kwargs)
        self.football_config = self.backend.ti.football
        self.tennis_config = self.backend.ti.tennis
        self.horseracing_config = self.backend.ti.horse_racing
        self.greyhound_racing_config = self.backend.ti.greyhound_racing
        self.tote_config = self.backend.ti.tote
        self.your_call_config = self.backend.ti.your_call
        self.virtuals_config = self.backend.ti.virtuals
        self.american_football_config = self.backend.ti.american_football
        self.baseball_config = self.backend.ti.baseball
        self.snooker_config = self.backend.ti.snooker
        self.ice_hockey_config = self.backend.ti.ice_hockey
        self.cricket_config = self.backend.ti.cricket
        self.volleyball_config = self.backend.ti.volleyball
        self.beach_volleyball_config = self.backend.ti.beach_volleyball
        self.rugby_union_config = self.backend.ti.rugby_union
        self.rugby_league_config = self.backend.ti.rugby_league
        self.darts_config = self.backend.ti.darts
        self.boxing_config = self.backend.ti.boxing
        self.gaelic_football_config = self.backend.ti.gaelic_football
        self.handball_config = self.backend.ti.handball
        self.basketball_config = self.backend.ti.basketball
        self.badminton_config = self.backend.ti.badminton
        self.golf_config = self.backend.ti.golf
        self.esports_config = self.backend.ti.esports
        self.event = None
        self.CREATED_EVENTS = []
        self.MODIFIED_EVENTS = []
        self.market_ids = OrderedDict()
        self.ss_timeout = self.backend.siteserve.general_info.timeout
        self.ss_version = kwargs.get('ss_version', '2.31')

    def looking_for_event_in_ss_response(self, event_id):
        from crlat_siteserve_client.siteserve_client import SiteServeRequests
        s = SiteServeRequests(env=self.env, brand=self.brand)
        event = s.ss_event_to_outcome_for_event(event_id=event_id, raise_exceptions=False, timeout=10)
        return event

    def _add_your_call_market_with_selections(self, event_id, your_call_market, template_name, template_id, **kwargs):
        selection_prefix = kwargs['selection_prefix'] if 'selection_prefix' in kwargs and kwargs['selection_prefix'] else generate_name()
        selections_count = kwargs['selections_count'] if 'selections_count' in kwargs.keys() else 1
        disporder = '-%s' % str(500 - selections_count)
        market_name = '%s%s' % (template_name, your_call_market)
        market_id = self.event.create_market(event_id=event_id, market_name=market_name, market_template_id=template_id,
                                             disporder=disporder)
        market_ids = {your_call_market: market_id}
        selection_ids = OrderedDict()

        for iteration in range(0, selections_count):
            iteration += 1
            selections = self.event.add_selections(selection_names=['%s %s' % (selection_prefix, str(iteration))],
                                                   prices=('%s/%s' % (iteration, iteration + 1),),
                                                   marketID=market_id,
                                                   selection_types='YC')
            selection_ids.update({your_call_market: selections})
        return market_ids, selection_ids

    def add_custom_markets_with_selections(self, event_id, markets, class_id, category_id, type_id,
                                           lp=None, private=False, **kwargs):
        if not self.event:
            self.event = CreateSportEvent(env=self.env, brand=self.brand, category_id=category_id, class_id=class_id, type_id=type_id)
        prices = lp if lp else self.event.prices
        all_selections = OrderedDict()
        all_markets = OrderedDict()
        scorecast_market = next((market for market in markets if market[0] == 'scorecast'), None)
        handicap_market = next((market for market in markets if market[0] == 'handicap'), None)
        match_result_and_over_under_market = next((market for market in markets if market[0] == 'match_result_and_over_under'), None)
        both_team_to_score_and_over_under_market = next((market for market in markets if market[0] == 'both_team_to_score_and_over_under'), None)
        if scorecast_market:
            market_properties = scorecast_market[1]
            markets.remove(scorecast_market)
            markets.extend([('correct_score', market_properties), ('first_goalscorer', market_properties),
                            ('last_goalscorer', market_properties), ('first_goal_scorecast', market_properties),
                            ('last_goal_scorecast', market_properties)])
        if handicap_market:
            market_properties = handicap_market[1]
            markets.remove(handicap_market)
            markets.extend([('handicap_match_result', market_properties), ('handicap_first_half', market_properties),
                            ('handicap_second_half', market_properties),
                            ('handicap_3_way', market_properties)])
        for market_ in (match_result_and_over_under_market, both_team_to_score_and_over_under_market):
            # handling the same market adding logic
            if market_:
                market_short_name = market_[0]
                market_properties = market_[1]
                markets.remove(market_)
                over_under = market_properties.get('over_under', None)
                if not isinstance(over_under, (list, tuple)):
                    over_under = [over_under] if over_under else ['2.5', '3.5', '4.5', '5.5', '6.5', '7.5', '8.5',
                                                                  '9.5', '10.5']
                else:
                    over_under = [str(o) for o in over_under]
                for over_under_value in over_under:
                    market_short_name_new = f'{market_short_name}_{str(over_under_value).replace(".", "_")}_goals'
                    market_properties_new = dict(market_properties)
                    market_properties_new.update({'over_under': over_under_value})
                    markets.append((market_short_name_new, market_properties_new))

        for market in markets:
            market_short_name = market[0]
            market_properties = market[1] if len(market) == 2 else OrderedDict()
            cashout = market_properties['cashout'] if 'cashout' in market_properties.keys() else False
            handicap = market_properties['handicap'] if 'handicap' in market_properties.keys() else 5
            over_under = None
            if 'over_under' in market_short_name and all((market_ not in market_short_name
                                                          for market_ in ('both_team_to_score_and_over_under',
                                                                          'match_result_and_over_under'))):
                over_under = market_properties['over_under'] if 'over_under' in market_properties.keys() else 1.5

            def get_markets_config(type_id_):
                return {
                    self.football_config.autotest_class.autotest_premier_league.type_id:
                        self.football_config.autotest_class.autotest_premier_league.markets,
                    self.football_config.autotest_class.autotest_league2.type_id:
                        self.football_config.autotest_class.autotest_league2.markets,
                    self.football_config.autotest_class.special_autotest_league.type_id:
                        self.football_config.autotest_class.special_autotest_league.markets,
                    self.football_config.spain.spanish_la_liga.type_id:
                        self.football_config.spain.spanish_la_liga.markets,
                    self.football_config.england.championship.type_id:
                        self.football_config.england.championship.markets,
                    self.football_config.italy_serie_a.serie_a.type_id:
                        self.football_config.italy_serie_a.serie_a.markets,
                    self.football_config.uefa_club_champions.uefa_champions_league.type_id:
                        self.football_config.uefa_club_champions.uefa_champions_league.markets,
                    self.football_config.england.premier_league.type_id:
                        self.football_config.england.premier_league.markets,
                    self.tennis_config.tennis_autotest.autotest_trophy.type_id:
                        self.tennis_config.tennis_autotest.autotest_trophy.markets,
                    self.darts_config.darts_autotest.championship_league.type_id:
                        self.darts_config.darts_autotest.championship_league.markets,
                    self.darts_config.darts_autotest.darts_autotest_handicap.type_id:
                        self.darts_config.darts_autotest.darts_autotest_handicap.markets,
                    self.rugby_league_config.rugby_league_all_rugby_league.super_league.type_id:
                        self.rugby_league_config.rugby_league_all_rugby_league.super_league.markets,
                    self.rugby_league_config.rugby_league_all_rugby_league.rugby_autotest_handicap.type_id:
                        self.rugby_league_config.rugby_league_all_rugby_league.rugby_autotest_handicap.markets,
                    self.rugby_union_config.rugby_union_all_rugby_union.world_cup.type_id:
                        self.rugby_union_config.rugby_union_all_rugby_union.world_cup.markets,
                    self.rugby_union_config.rugby_union_all_rugby_union.rugby_autotest_handicap.type_id:
                        self.rugby_union_config.rugby_union_all_rugby_union.rugby_autotest_handicap.markets,
                    self.ice_hockey_config.ice_hockey_usa.ahl.type_id:
                        self.ice_hockey_config.ice_hockey_usa.ahl.markets,
                    self.ice_hockey_config.ice_hockey_usa.icehockey_autotest_handicap.type_id:
                        self.ice_hockey_config.ice_hockey_usa.icehockey_autotest_handicap.markets,
                    self.golf_config.golf_all_golf.allianz_championship.type_id:
                        self.golf_config.golf_all_golf.allianz_championship.markets,
                    self.basketball_config.basketball_usa.nba.type_id:
                        self.basketball_config.basketball_usa.nba.markets,
                    self.basketball_config.basketball_autotest.basketball_autotest_total_points.type_id:
                        self.basketball_config.basketball_autotest.basketball_autotest_total_points.markets,
                    self.american_football_config.american_football_autotest.autotest_league.type_id:
                        self.american_football_config.american_football_autotest.autotest_league.markets,
                    self.american_football_config.american_football_autotest.american_football_autotest_handicap.type_id:
                        self.american_football_config.american_football_autotest.american_football_autotest_handicap.markets,
                    self.volleyball_config.volleyball_austria.avl.type_id:
                        self.volleyball_config.volleyball_austria.avl.markets,
                    self.volleyball_config.volleyball_austria.avl_set_handicap.type_id:
                        self.volleyball_config.volleyball_austria.avl_set_handicap.markets,
                    self.snooker_config.snooker_all_snooker.world_championship.type_id:
                        self.snooker_config.snooker_all_snooker.world_championship.markets,
                    self.baseball_config.baseball_autotest.autotest_league.type_id:
                        self.baseball_config.baseball_autotest.autotest_league.markets,
                    self.baseball_config.baseball_autotest.autotest_handicap.type_id:
                        self.baseball_config.baseball_autotest.autotest_handicap.markets,
                    self.cricket_config.cricket_all_cricket.cricket_autotest.type_id:
                        self.cricket_config.cricket_all_cricket.cricket_autotest.markets,
                    self.cricket_config.cricket_all_cricket.cricket_autotest_total_sixes.type_id:
                        self.cricket_config.cricket_all_cricket.cricket_autotest_total_sixes.markets
                }.get(type_id_, {})

            market_template_ids = get_markets_config(type_id)
            try:
                inner_dict = market_template_ids[market_short_name]
            except KeyError as err:
                raise OBException('%s is not found in list of known football market templates: %s' %
                                  (err, ', '.join(market_template_ids.keys())))
            if inner_dict is None:
                raise OBException(f'Could not get market template id for market: "{market_short_name}", '
                                  f'need to check crlat_backend_config_{self.brand}.yaml file content')
            template_name, template_id = list(inner_dict.items())[0]
            disporder = market_properties['disp_order'] if 'disp_order' in market_properties.keys() \
                else self.event._find_disporder_for_market(template_id)
            if template_name in ('|Total Goals|',
                                 '|Over/Under Total Goals|',
                                 '|Over/Under First Half|',
                                 '|Over/Under Second Half|'):
                template_name = '%s |%s|' % (template_name, over_under)

            if market_short_name == 'your_call':
                yc_market_ids, yc_selection_ids = OrderedDict(), OrderedDict()
                your_call_market = next((market for market in markets if market[0] == 'your_call'), None)
                selection_prefix = your_call_market[1]['selection_prefix'] \
                    if len(your_call_market) > 1 and 'selection_prefix' in your_call_market[1] else None
                for yc_market in self.football_config.your_call_markets:
                    market_ids, selection_ids = self._add_your_call_market_with_selections(
                        event_id=event_id,
                        your_call_market=yc_market,
                        template_name=template_name,
                        template_id=template_id,
                        selections_count=self.football_config.your_call_markets.index(yc_market) + 1,
                        selection_prefix=selection_prefix, **kwargs)
                    yc_market_ids.update(market_ids)
                    yc_selection_ids.update(selection_ids)
                all_markets.update({market_short_name: yc_market_ids})
                all_selections.update({market_short_name: yc_selection_ids})

            elif market_short_name in ['handicap_match_result',
                                       'handicap_first_half',
                                       'handicap_second_half',
                                       'handicap_3_way']:
                for m in range(1, 4):  # m is handicap_index
                    for sign in ['+', '-']:
                        market_name = template_name.replace('_placeholder_',
                                                            '- %s| %s|%.1f| |goals' % (self.event.team1_name, sign, m))
                        handicap = sign + '%.1f' % m
                        market_id = self.event.create_market(event_id=event_id, market_name=market_name,
                                                             market_template_id=template_id,
                                                             cashout=cashout, handicap=handicap, private=private)
                        selections = self.event.add_handicap_selection(odds_home='%d/%d' % (m + 1, m + 2),
                                                                       odds_draw='%d/%d' % (m + 3, m + 2),
                                                                       odds_away='%d/%d' % (m + 4, m + 1),
                                                                       marketID=market_id)
                        all_markets.update({market_short_name + ' ' + handicap: market_id})
                        all_selections.update({market_short_name + ' ' + handicap: selections})

            elif any((market_ in market_short_name for market_ in
                      ('match_result_and_over_under', 'both_team_to_score_and_over_under'))):
                over_under = market_properties.get('over_under')
                market_name = template_name.replace(f' {over_under} ', f'| |{over_under}| |')
                market_id = self.event.create_market(event_id=event_id,
                                                     market_name=market_name,
                                                     market_template_id=template_id,
                                                     cashout=cashout,
                                                     private=private,
                                                     **kwargs)
            elif "lucky_dip" in market_short_name:
                market_id,selections=self.event.add_lucky_dip_market_and_selection(event_id=event_id, market_name=template_name,
                                                     market_template_id=template_id,
                                                     cashout=cashout,disporder=disporder,bet_in_run="N",market_displayed=True,selection_names=kwargs.get("selection_names"),**kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
                return all_selections, all_markets
            else:  # all other markets
                is_over_under = True if market_short_name in ['over_under_total_goals',
                                                              'over_under_first_half',
                                                              'over_under_second_half',
                                                              'total_180s_over_under',
                                                              'total_180s_over_under_1',
                                                              'over_under_home_team_total_goals',
                                                              'over_under_away_team_total_goals',
                                                              'over_under_first_half_home_team_total_goals',
                                                              'over_under_first_half_away_team_total_goals',
                                                              'over_under_second_half_home_team_total_goals',
                                                              'over_under_second_half_away_team_total_goals'] else None
                market_id = self.event.create_market(event_id=event_id, market_name=template_name,
                                                     market_template_id=template_id,
                                                     cashout=cashout, handicap=handicap,
                                                     private=private, over_under=over_under,
                                                     is_over_under=is_over_under, disporder=disporder, **kwargs)
            # ADDING SPECIFIC SELECTIONS NOW
            if market_short_name not in ['total_goals',
                                         'total_points',
                                         'total_points_1',
                                         'total_sixes',
                                         'total_sixes_2',
                                         'total_sixes_3',
                                         '60_minute_betting',
                                         'next_over_runs',
                                         'team_runs',
                                         'runs_at_fall_of_next_wicket',
                                         'home_team_total_points',
                                         'home_team_total_points_2',
                                         'away_team_total_points',
                                         'away_team_total_points_2',
                                         'half_total_points',
                                         'half_total_points_2',
                                         'quarter_total_points',
                                         'quarter_total_points_2',
                                         'over_under_total_goals',
                                         'over_under_first_half',
                                         'over_under_second_half',
                                         'over_under_home_team_total_goals',
                                         'over_under_away_team_total_goals',
                                         'over_under_first_half_home_team_total_goals',
                                         'over_under_first_half_away_team_total_goals',
                                         'over_under_second_half_home_team_total_goals',
                                         'over_under_second_half_away_team_total_goals',
                                         'total_goals_2_way',
                                         'total_goals_2_way_2',
                                         'total_180s_over_under',
                                         'total_180s_over_under_1',
                                         'total_match_points',
                                         'correct_score',
                                         'first_half_correct_score',
                                         'second_half_correct_score',
                                         'handicap',
                                         'handicap_match_result',
                                         'handicap_first_half',
                                         'handicap_second_half',
                                         'handicap_3_way',
                                         'both_teams_to_score',
                                         'first_goalscorer',
                                         'last_goalscorer',
                                         'last_goal_scorecast',
                                         'first_goal_scorecast',
                                         'goalscorer_2_or_more',
                                         'anytime_goalscorer',
                                         'first_half_result',
                                         'second_half_result',
                                         'hat_trick',
                                         'double_chance',
                                         'half_time_double_chance',
                                         'second_half_double_chance',
                                         'score_goal_in_both_halves',
                                         'your_call',
                                         'match_result_and_over_under_2_5_goals',
                                         'match_result_and_over_under_3_5_goals',
                                         'match_result_and_over_under_4_5_goals',
                                         'match_result_and_over_under_5_5_goals',
                                         'match_result_and_over_under_6_5_goals',
                                         'match_result_and_over_under_7_5_goals',
                                         'match_result_and_over_under_8_5_goals',
                                         'match_result_and_over_under_9_5_goals',
                                         'match_result_and_over_under_10_5_goals',
                                         'both_team_to_score_and_over_under_2_5_goals',
                                         'both_team_to_score_and_over_under_3_5_goals',
                                         'both_team_to_score_and_over_under_4_5_goals',
                                         'both_team_to_score_and_over_under_5_5_goals',
                                         'both_team_to_score_and_over_under_6_5_goals',
                                         'both_team_to_score_and_over_under_7_5_goals',
                                         'both_team_to_score_and_over_under_8_5_goals',
                                         'both_team_to_score_and_over_under_9_5_goals',
                                         'both_team_to_score_and_over_under_10_5_goals',
                                         'total_frames_over_under',
                                         'total_runs',
                                         'total_runs_1',
                                         'match_handicap',
                                         'match_handicap_1',
                                         'match_handicap_2',
                                         'total_match_points_1',
                                         'total_match_points_2',
                                         'sixty_minutes_betting'
                                         ]:
                # markets with only two selections. #todo: VOL-552 list is probably needed to be extended.
                if market_short_name in ['handicap_2_way', 'handicap_2_way_2', 'handicap_2_way_3', 'to_qualify',
                                         'to_win_not_to_nil', 'to_win_to_nil',
                                         'draw_no_bet', 'half_time_draw_no_bet', 'second_half_draw_no_bet', 'penalty_shoot_out_winner', 'match_set_handicap', 'match_set_handicap_2']:
                    selections = self.event.add_selections(prices=self.event.other_sport_prices, marketID=market_id,
                                                           selection_names=('|%s|' % self.event.team1_name,
                                                                            '|%s|' % self.event.team2_name),
                                                           selection_types=('H', 'A'),
                                                           **kwargs)
                elif market_short_name == 'half_time_full_time':
                        prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, 9)]
                        selections = self.event.add_selections(prices=prices,
                                                               selection_names=(
                                                               '|%s||/||%s|' % (self.event.team1_name,
                                                                                   self.event.team1_name),
                                                               '|%s||/||Draw|' % self.event.team1_name,
                                                               '|%s||/||%s|' % (self.event.team1_name,
                                                                                self.event.team2_name),
                                                               '|Draw||/||%s|' % self.event.team1_name,
                                                               '|Draw||/||Draw|',
                                                               '|Draw||/||%s|' % self.event.team2_name,
                                                               '|%s||/||%s|' % (self.event.team2_name,
                                                                                self.event.team1_name),
                                                               '|%s||/||Draw|' % self.event.team2_name,
                                                               '|%s||/||%s|' % (self.event.team2_name,
                                                                                self.event.team2_name),
                                                               ),
                                                               selection_types=('1', '2', '3', '4', '5', '6', '7', '8', '9'),
                                                               marketID=market_id, **kwargs)
                        all_markets.update({market_short_name: market_id})
                        all_selections.update({market_short_name: selections})
                else:
                    selections = self.event.add_selections(prices=prices, marketID=market_id, **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if market_short_name == 'score_goal_in_both_halves':
                selections = self.event.add_selections(prices=self.event.other_sport_prices, marketID=market_id,
                                                       selection_names=('|Yes|', '|No|'),
                                                       selection_types=('H', 'A'), **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if 'double_chance' in market_short_name:
                selections = self.event.add_selections(prices=prices,
                                                       selection_names=('|%s|| or ||Draw|' % self.event.team1_name,
                                                                        '|%s|| or ||Draw|' % self.event.team2_name,
                                                                        '|%s|| or ||%s|' % (self.event.team1_name,
                                                                                            self.event.team2_name)),
                                                       selection_types=('1', '2', '3'),
                                                       marketID=market_id, **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if market_short_name in ['total_match_points', 'total_match_points_1', 'total_match_points_2']:
                selections = self.event.add_selections(prices=self.event.other_sport_prices, marketID=market_id,
                                                       selection_names=('|%s|' % self.event.team1_name,
                                                                        '|%s|' % self.event.team2_name),
                                                       selection_types=('H', 'L'),
                                                       **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if market_short_name in ['first_goalscorer',
                                     'last_goalscorer',
                                     'goalscorer_2_or_more',
                                     'anytime_goalscorer',
                                     'hat_trick']:
                for i in range(0, 9):
                    if bool(i & 1):
                        player_type = 'H'
                    else:
                        player_type = 'A'
                    selections = self.event.add_selections(prices=prices,
                                                           marketID=market_id,
                                                           selection_names='|Player %s|' % (i + 1),
                                                           selection_types=player_type,
                                                           **kwargs
                                                           )
                    all_markets.update({market_short_name: market_id})
                    all_selections.update({market_short_name: selections})
            if market_short_name in ['last_goal_scorecast', 'first_goal_scorecast',]:
                # this markets are 'technical' so scorecast market will be shown
                # and no selections should be added here
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: {}})

            if market_short_name in ['first_half_result', 'second_half_result']:
                prices = {
                    'odds_home': '1/1',
                    'odds_draw': '3/1',
                    'odds_away': '4/1'
                }
                selection_names = ['|0-1|', '|2|', '|3+|']
                selections = self.event.add_selections(marketID=market_id, prices=prices.values(),
                                                       selection_names=selection_names, **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if market_short_name in ['total_goals', 'match_handicap', 'match_handicap_1', 'match_handicap_2']:
                selections = self.event.add_selections(prices=prices, marketID=market_id,
                                                       selection_names=('|Over|', '|Under|'),
                                                       selection_types=('H', 'A'), **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if market_short_name in ['over_under_total_goals',
                                     'over_under_first_half',
                                     'over_under_second_half',
                                     'total_goals_2_way',
                                     'total_goals_2_way_2',
                                     'total_points',
                                     'total_points_1',
                                     'total_sixes',
                                     'total_sixes_2',
                                     'total_sixes_3',
                                     'next_over_runs',
                                     'team_runs',
                                     'runs_at_fall_of_next_wicket',
                                     'home_team_total_points',
                                     'home_team_total_points_2',
                                     'away_team_total_points',
                                     'away_team_total_points_2',
                                     'half_total_points',
                                     'half_total_points_2',
                                     'quarter_total_points',
                                     'quarter_total_points_2',
                                     'total_frames_over_under',
                                     'total_runs',
                                     'total_runs_1',
                                     'total_180s_over_under',
                                     'total_180s_over_under_1',
                                     'over_under_home_team_total_goals',
                                     'over_under_away_team_total_goals',
                                     'over_under_first_half_home_team_total_goals',
                                     'over_under_first_half_away_team_total_goals',
                                     'over_under_second_half_home_team_total_goals',
                                     'over_under_second_half_away_team_total_goals']:
                selections = self.event.add_selections(marketID=market_id,
                                                       selection_names=('|Over|', '|Under|'),
                                                       prices=('1/2', '2/1'),
                                                       selection_types=('H', 'L'), **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})

            if market_short_name in ['correct_score', 'first_half_correct_score', 'second_half_correct_score']:
                selections = self.event.add_correct_score_selections(prices=self.event.correct_score_prices,
                                                                     marketID=market_id, **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})

            if market_short_name == 'both_teams_to_score':
                selections = self.event.add_both_team_to_score_selection(marketID=market_id,
                                                                         selection_names=('|Yes|', '|No|'),
                                                                         prices=('1/2', '1/2'), **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if 'match_result_and_over_under' in market_short_name:
                selection_names = []
                for over_under_selection_name in (self.event.team1_name, self.event.team2_name, 'Draw'):
                    for over_or_under_label_name in ('Over', 'Under'):
                            selection_names.append(f'|{over_under_selection_name}| |and {over_or_under_label_name} {over_under} Goals|')
                prices = [f'{Faker().random_int(min=1, max=10)}/{Faker().random_int(min=1, max=20)}' for _ in selection_names]
                selection_types = ['A'] * len(prices)  # actually, selection_types is not needed at all, but otherwise add_selections will fail
                selections = self.event.add_selections(prices=prices,
                                                       marketID=market_id,
                                                       selection_names=selection_names,
                                                       selection_types=selection_types,
                                                       **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if 'both_team_to_score_and_over_under' in market_short_name:
                selection_names = []
                for over_under_selection_name in ('Yes', 'No'):
                    for over_or_under_label_name in ('Over', 'Under'):
                            selection_names.append(f'|{over_under_selection_name} and {over_or_under_label_name} {over_under} Goals|')
                prices = [f'{Faker().random_int(min=1, max=10)}/{Faker().random_int(min=1, max=20)}' for _ in selection_names]
                selection_types = ['A'] * len(prices)  # actually, selection_types is not needed at all, but otherwise add_selections will fail
                selections = self.event.add_selections(prices=prices,
                                                       marketID=market_id,
                                                       selection_names=selection_names,
                                                       selection_types=selection_types,
                                                       **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})
            if market_short_name in ['60_minute_betting', 'sixty_minutes_betting']:
                selections = self.event.add_selections(prices=self.event.prices,
                                                       selection_names=('|%s|' % self.event.team1_name,
                                                                        '|Draw|',
                                                                        '|%s|' % self.event.team2_name),
                                                       selection_types=['H', 'D', 'A'],
                                                       marketID=market_id, **kwargs)
                all_markets.update({market_short_name: market_id})
                all_selections.update({market_short_name: selections})

        return all_selections, all_markets

    def _get_racing_market_template_name_and_id(self, market_short_name, type_id) -> tuple:
        """
        Internal method to get market template name and it's id by market short name and racing type
        :param market_short_name:
        :param type_id:
        :return:
        """
        racing_live = self.horseracing_config.horse_racing_live
        greyhound_racing_live = self.greyhound_racing_config.greyhounds_live

        def get_markets_config(type_id_):
            return {
                racing_live.autotest_uk.type_id:
                    racing_live.autotest_uk.markets,
                racing_live.autotest_international.type_id:
                    racing_live.autotest_international.markets,
                racing_live.autotest_virtual.type_id:
                    racing_live.autotest_virtual.markets,
                greyhound_racing_live.autotest.type_id:
                    greyhound_racing_live.autotest.markets
            }.get(type_id_, {})

        market_template_ids = get_markets_config(type_id)
        try:
            inner_dict = market_template_ids[market_short_name]
        except KeyError as err:
            raise OBException('%s is not found in list of known horse racing market templates: %s' %
                              (err, ', '.join(market_template_ids.keys())))

        if inner_dict is None:
            raise OBException(f'Could not get market template id for market: "{market_short_name}", '
                              f'need to check crlat_backend_config_{self.brand}.yaml file content')
        template_name, template_id = list(inner_dict.items())[0]
        return template_name, template_id

    def add_racing_markets_with_selections(self, event_id, markets, class_id, category_id, type_id, runner_names,
                                           lp_prices=None, **kwargs):
        if not self.event:
            self.event = CreateRacingEvent(env=self.env, brand=self.brand, category_id=category_id, class_id=class_id, type_id=type_id)
        all_selections = OrderedDict()
        all_markets = OrderedDict()

        for market in markets:
            market_short_name = market[0]
            market_properties = market[1] if len(market) == 2 else OrderedDict()
            cashout = market_properties['cashout'] if 'cashout' in market_properties.keys() else False
            without_runner = market_properties.get('without_runner') if market_properties.get(
                'without_runner') else False  # mostly for betting_without market

            template_name, template_id = self._get_racing_market_template_name_and_id(market_short_name=market_short_name,
                                                                                      type_id=type_id)

            market_name_ = '%s %s' % (template_name, runner_names[int(without_runner) - 1]) \
                if market_short_name == 'betting_without' and without_runner else template_name
            lp = True if lp_prices else False
            if not lp:
                lp = kwargs.get('lp', False)
            kwargs.pop('lp', None)
            market_id = self.event.create_market(event_id=event_id, market_name=market_name_,
                                                 market_template_id=template_id,
                                                 cashout=cashout, lp=lp, **kwargs)
            for i, name in enumerate(runner_names):
                if int(without_runner) == i + 1:
                    continue
                else:
                    self.event.add_selections(market_id=market_id, runner_number=i + 1, name=name, price=lp_prices[i]) \
                        if lp_prices else self.event.add_selections(runner_number=i + 1, name=name, **kwargs)

            selections = self.event.get_selection_ids(marketID=market_id)
            all_markets[market_short_name] = market_id
            all_selections[market_short_name] = selections
        return all_selections, all_markets

    def add_sport_event(self, class_id, category_id, type_id, market_template_id, cashout=True,
                        lp=None, markets=None, default_market_name=None,
                        start_time=None, is_live=False, is_tomorrow=False, is_off=None, is_upcoming=False, timeout=None,
                        wait_for_event=True, **kwargs):
        response = None
        if default_market_name:
            default_market_name = default_market_name
        else:
            if self.brand == 'bma':
                default_market_name = '|Match Result|'
            else:
                default_market_name = '|Match Betting|'

        self.event = CreateSportEvent(env=self.env, brand=self.brand, category_id=category_id, class_id=class_id, type_id=type_id,
                                      market_template_id=market_template_id, market_name=default_market_name)
        eventID, team1, team2, event_date_time = self.event.create_event(cashout=cashout, start_time=start_time,
                                                                         is_upcoming=is_upcoming, is_live=is_live,
                                                                         is_tomorrow=is_tomorrow, is_off=is_off,
                                                                         **kwargs)
        self.CREATED_EVENTS.append(eventID)
        all_markets_ids = OrderedDict()
        default_market = 'enhanced_multiples' if default_market_name == '|Enhanced Multiples|' \
            else default_market_name.replace('|', '').replace(' ', '_').lower()

        prices = lp if lp else self.event.prices if category_id in [9, 10, 16, 20, 53, 31, 30, 54, 18, 13] else self.event.other_sport_prices

        if default_market_name in ['|Match Result|', '|Match Betting|']:
            market_template_id = kwargs.get('market_template_id', self.event.market_template_id)
            market_disporder = kwargs.get('disporder', self.event._find_disporder_for_market(market_template_id))
            market_class = WinDrawWinMarket if category_id in [10, 16, 20, 53, 31, 30, 54, 13] else WinWinMarket
            market_entity = market_class(eventID=eventID, market_name=default_market_name,
                                         market_disporder=market_disporder, market_template_id=market_template_id,
                                         prices=prices, home_name=team1, away_name=team2)
            self.event.create_multiple_markets(markets=[market_entity], **kwargs)
            event_markets = self.event.get_markets_for_event()
            default_marketID = event_markets.get(default_market_name)
            if not default_marketID:
                raise OBException(f'Cannot find market {default_market_name} in "{event_markets.keys()}"')
            self.event.update_market_settings(market_id=default_marketID, cashout=cashout, bet_in_run='Y',
                                              market_display_sort_code=market_entity.market_display_sort_code, **kwargs)
        else:
            default_marketID = self.event.create_market(cashout=cashout, bet_in_run='Y', event_id=eventID, **kwargs) \
                if is_live or is_upcoming else self.event.create_market(cashout=cashout, **kwargs)

        self.market_ids[eventID] = {default_market: default_marketID}
        all_selections = OrderedDict()
        if default_market_name == '|Enhanced Multiples|':
            type = kwargs['selection_type'] if 'selection_type' in kwargs.keys() else "all to win in 90 Mins"
            selections = self.event.add_enhanced_multiples_selection(odds='2',
                                                                     marketID=default_marketID,
                                                                     selection_name='|' + team1 + ', ' + team2 + '| ' + type,
                                                                     **kwargs)
        elif default_market_name == '|Outright|':
            selections_number = kwargs.get('selections_number', 5)
            selection_types = ['A'] * selections_number  # actually, selection_types is not needed at all, but otherwise add_selections will fail
            selection_names = kwargs.get('selections_names', ['|Auto test %s|' % generate_name() for _ in range(0, selections_number)])
            prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, selections_number)]
            selections = self.event.add_selections(prices=prices,
                                                   marketID=default_marketID,
                                                   selection_names=selection_names,
                                                   selection_types=selection_types, **kwargs)
        elif default_market_name in ['|Match Result|', '|Match Betting|']:
            # selections are created already via multiple markets creation
            selections = self.event.get_selection_ids(marketID=default_marketID)
            if not selections:
                raise OBException(f'Not all selections were added to market id {default_marketID}')
            max_mult_bet = kwargs.get('max_mult_bet') if 'max_mult_bet' in kwargs else ""
            min_bet = kwargs.get('min_bet') if 'min_bet' in kwargs else ""
            max_bet = kwargs.get('max_bet') if 'max_bet' in kwargs else ""
            for selection in list(selections.values()):
                self.change_min_max_bet_limits(id=selection, level='selection', min_bet=min_bet,
                                               max_bet=max_bet, max_mult_bet=max_mult_bet)
        elif default_market_name in ['|Total Sixes|', '|Total Points|']:
            selections = self.event.add_selections(prices=self.event.other_sport_prices,
                                                   marketID=default_marketID,
                                                   selection_names=('|Over|', '|Under|'),
                                                   selection_types=('H', 'L'), **kwargs)
        elif default_market_name in ['|Match Betting Head/Head|', '|Handicap 2-way|', '|Match Handicap|']:
            selections = self.event.add_selections(prices=self.event.other_sport_prices,
                                                   marketID=default_marketID,
                                                   selection_names=('|%s|' % self.event.team1_name,
                                                                    '|%s|' % self.event.team2_name),
                                                   selection_types=('H', 'A'), **kwargs)
        else:
            selections = self.event.add_selections(prices=prices, marketID=default_marketID, **kwargs)
        if 'special' in kwargs and kwargs['special']:
            self.make_market_special(event_id=eventID, market_id=default_marketID,
                                     market_template_id=market_template_id)

        if markets:
            all_selections, all_markets = \
                self.add_custom_markets_with_selections(event_id=eventID, markets=markets, class_id=class_id,
                                                        category_id=category_id,
                                                        type_id=type_id, lp=prices, **kwargs)
            all_markets.update({default_market: default_marketID})
            all_markets_ids.update({eventID: all_markets})
            self.market_ids[eventID].update(all_markets_ids[eventID])

        all_selections.update({default_market: selections})

        if wait_for_event:
            from crlat_siteserve_client.siteserve_client import SiteServeRequests
            s = SiteServeRequests(env=self.env, class_id=class_id, version=self.ss_version,
                                  category_id=category_id, brand=self.brand)
            ss_timeout_ = timeout if timeout else self.ss_timeout
            wait_for_result(lambda: self._get_number_of_selections_in_ss_response(event_id=eventID) == sum(len(market_selections.values())
                                                                                                           for market_name, market_selections in all_selections.items()),
                            name='Event selections to be available on SiteServe',
                            bypass_exceptions=(KeyError, IndexError, AttributeError),
                            poll_interval=2,
                            timeout=ss_timeout_)
            response = s.ss_event_to_outcome_for_event(event_id=eventID,
                                                       query_builder=query_builder().add_filter(translation_lang()))[0]

        selection_ids = all_selections if markets else all_selections[default_market]
        Parameters = namedtuple('event_parameters',
                                ['event_id', 'team1', 'team2', 'selection_ids', 'event_date_time',
                                 'default_market_id', 'all_markets_ids', 'ss_response'])
        event_params = Parameters(eventID, team1, team2, selection_ids, event_date_time,
                                  default_marketID, all_markets_ids, response)
        return event_params

    def _get_number_of_selections_in_ss_response(self, event_id):
        ss_event = self.looking_for_event_in_ss_response(event_id=event_id)
        number_of_selections = sum([len(market.get('market', {}).get('children', [])) for market in ss_event[0].get('event', {}).get('children', [])])
        return number_of_selections

    def add_racing_event(self, class_id, category_id, type_id, market_template_id, default_market_name,
                         event_name_pattern=None, number_of_runners=5, markets=None, ew_terms=None, cashout=True,
                         specials=False, lp_prices=None, forecast_available=False, tricast_available=False,
                         is_tomorrow=False, is_live=False, timeout=None, wait_for_event=True, **kwargs):
        """
        :param ew_terms: dictionary with the following keys:
            ew_places, ew_fac_num, ew_fac_den
        """
        response = None
        r = CreateRacingEvent(env=self.env, brand=self.brand, category_id=category_id, class_id=class_id, type_id=type_id,
                              market_template_id=market_template_id, market_name=default_market_name,
                              event_name_pattern=event_name_pattern)
        eventID, event_off_time, event_date_time = r.create_event(is_tomorrow=is_tomorrow, is_live=is_live,
                                                                   cashout=cashout, **kwargs)
        self.CREATED_EVENTS.append(eventID)
        lp = True if lp_prices else False
        if not lp:
            lp = kwargs.get('lp', False)
        kwargs.pop('lp', None)
        min_bet = kwargs.get('min_bet', '')
        max_bet = kwargs.get('max_bet', '')
        default_marketID = r.create_market(cashout=cashout, bet_in_run=is_live, ew_terms=ew_terms, specials=specials,
                                           forecast_available=forecast_available, tricast_available=tricast_available,
                                           lp=lp, **kwargs)
        self.market_ids[eventID] = default_marketID
        default_market = default_market_name.replace('|', '').replace(' ', '_').lower()
        runner_numbers = kwargs.get('runner_numbers', None)
        number_of_runners = len(runner_numbers) if runner_numbers else number_of_runners
        runner_names = kwargs['runner_names'] if 'runner_names' in kwargs and kwargs['runner_names'] is not None \
            else [generate_name() for i in range(number_of_runners)]
        for i, name in enumerate(runner_names):
            runner_num = runner_numbers[i] if runner_numbers else i + 1
            r.add_selections(runner_number=runner_num, name=name, price=lp_prices[i], min_bet=min_bet, max_bet=max_bet) if lp_prices \
                else r.add_selections(runner_number=runner_num, name=name, **kwargs)

        if 'unnamed_favorites' in kwargs:
            number_of_runners += 2
            unnames_selection = {1: '|Unnamed Favourite|', 2: '|Unnamed 2nd Favourite|'}
            for unnamed_favorites_position, name in unnames_selection.items():
                r.add_selections(name=name, price=lp_prices[i]) if lp_prices else r.add_selections(name=name, **kwargs)
                selection_ids = r.get_selection_ids()
                r.change_racing_selection_type(id=selection_ids[name.strip('|')],
                                               unnamed_favorites_position=unnamed_favorites_position)

        selection_ids = r.get_selection_ids()
        all_selections = OrderedDict()
        all_markets = OrderedDict()

        if markets:
            all_selections, all_markets = \
                self.add_racing_markets_with_selections(event_id=eventID, markets=markets, class_id=class_id,
                                                        category_id=category_id, type_id=type_id, lp_prices=lp_prices,
                                                        forecast_available=forecast_available,
                                                        tricast_available=tricast_available,
                                                        runner_names=runner_names, **kwargs)
            all_markets.update({default_market: default_marketID})

        all_selections[default_market] = selection_ids
        self.market_ids.update(all_markets)
        selection_ids = all_selections if markets else all_selections[default_market]

        if all((forecast_available, tricast_available)):
            self._add_dividend_to_market(category_id=category_id, type_id=type_id, event_id=eventID,
                                         default_market_template_id=market_template_id,
                                         default_market_name=default_market_name, selection_ids=selection_ids, **kwargs)

        if wait_for_event:
            from crlat_siteserve_client.siteserve_client import SiteServeRequests
            s = SiteServeRequests(env=self.env, brand=self.brand)

            ss_timeout_ = timeout if timeout else self.ss_timeout
            wait_for_result(lambda: self._get_number_of_selections_in_ss_response(event_id=eventID) == sum(len(market_selections.values())
                                                                                                           for market_name, market_selections in all_selections.items()),
                            name='Event selections to be available on SiteServe',
                            bypass_exceptions=(KeyError, IndexError, AttributeError),
                            poll_interval=2,
                            timeout=ss_timeout_)
            response = s.ss_event_to_outcome_for_event(event_id=eventID,
                                                       query_builder=query_builder().add_filter(translation_lang()))[0]
        Parameters = namedtuple('event_parameters',
                                ['event_id', 'event_off_time', 'market_id', 'selection_ids',
                                 'event_date_time', 'all_markets_ids', 'ss_response'])
        event_params = Parameters(eventID, event_off_time, default_marketID, selection_ids,
                                  event_date_time, all_markets, response)
        return event_params

    def add_autotest_premier_league_football_event(self, start_time=None, markets=None, cashout=True,
                                                   is_live=False, is_upcoming=False, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.autotest_class.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.autotest_class.autotest_premier_league.type_id,
                                    markets=markets,
                                    market_template_id=self.football_config.autotest_class.autotest_premier_league.market_template_id,
                                    start_time=start_time, cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_premier_league_football_outright_event(self, start_time=None, markets=None, cashout=True,
                                                            is_live=False, is_upcoming=False, wait_for_event=True,
                                                            **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.football_config.autotest_class.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.autotest_class.autotest_premier_league.type_id,
                                    markets=markets,
                                    market_template_id=self.football_config.autotest_class.autotest_premier_league.outright_market_template_id,
                                    default_market_name=self.football_config.autotest_class.autotest_premier_league.outright_market_name,
                                    start_time=start_time,
                                    cashout=cashout,
                                    is_live=is_live,
                                    is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event,
                                    event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_football_event_enhanced_multiples(self, start_time=None, is_live=False,
                                              selection_type='all to win in 90 Mins', wait_for_event=True):
        return self.add_sport_event(class_id=self.football_config.specials.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.specials.enhanced_multiples.type_id,
                                    market_template_id=self.football_config.specials.enhanced_multiples.market_template_id,
                                    default_market_name=self.football_config.specials.enhanced_multiples.market_name,
                                    start_time=start_time, is_live=is_live, selection_type=selection_type,
                                    wait_for_event=wait_for_event)

    def add_football_event_to_special_league(self, markets=None, cashout=True, start_time=None, is_live=False,
                                             wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.autotest_class.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.autotest_class.special_autotest_league.type_id,
                                    market_template_id=self.football_config.autotest_class.special_autotest_league.market_template_id,
                                    default_market_name=self.football_config.autotest_class.special_autotest_league.market_name,
                                    markets=markets, start_time=start_time, cashout=cashout, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_football_event_to_spanish_la_liga(self, start_time=None, markets=None, cashout=True, is_live=False,
                                              is_upcoming=False, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.spain.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.spain.spanish_la_liga.type_id,
                                    market_template_id=self.football_config.spain.spanish_la_liga.market_template_id,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    markets=markets, start_time=start_time, wait_for_event=wait_for_event, **kwargs)

    def add_spain_la_liga_football_outright_event(self, start_time=None, markets=None, cashout=True,
                                                           is_live=False, is_upcoming=False, wait_for_event=True,
                                                           **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.football_config.spain.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.spain.spanish_la_liga.type_id,
                                    markets=markets,
                                    market_template_id=self.football_config.spain.spanish_la_liga.outright_market_template_id,
                                    default_market_name=self.football_config.spain.spanish_la_liga.outright_market_name,
                                    start_time=start_time,
                                    cashout=cashout,
                                    is_live=is_live,
                                    is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event,
                                    event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_football_event_to_england_championship(self, cashout=True, start_time=None, is_live=False, is_upcoming=False,
                                                   markets=None, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.england.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.england.championship.type_id,
                                    market_template_id=self.football_config.england.championship.market_template_id,
                                    cashout=cashout, start_time=start_time, wait_for_event=wait_for_event,
                                    is_live=is_live, is_upcoming=is_upcoming, markets=markets, **kwargs)

    def add_football_event_to_italy_serie_a(self, cashout=True, start_time=None, is_live=False, is_upcoming=False,
                                            markets=None, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.italy_serie_a.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.italy_serie_a.serie_a.type_id,
                                    market_template_id=self.football_config.italy_serie_a.serie_a.market_template_id,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    markets=markets, start_time=start_time, wait_for_event=wait_for_event, **kwargs)

    def add_football_event_to_uefa_champions_league(self, cashout=True, start_time=None, is_live=False,
                                                    is_upcoming=False,
                                                    markets=None, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.uefa_club_champions.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.uefa_club_champions.uefa_champions_league.type_id,
                                    market_template_id=self.football_config.uefa_club_champions.uefa_champions_league.market_template_id,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming, markets=markets,
                                    start_time=start_time,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_football_event_to_england_premier_league(self, cashout=True, start_time=None, is_live=False,
                                                     is_upcoming=False,
                                                     markets=None, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.football_config.england.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.england.premier_league.type_id,
                                    market_template_id=self.football_config.england.premier_league.market_template_id,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    markets=markets, start_time=start_time, wait_for_event=wait_for_event, **kwargs)

    def add_england_premier_league_football_outright_event(self, start_time=None, markets=None, cashout=True,
                                                           is_live=False, is_upcoming=False, wait_for_event=True,
                                                           **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.football_config.england.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.england.premier_league.type_id,
                                    markets=markets,
                                    market_template_id=self.football_config.england.premier_league.outright_market_template_id,
                                    default_market_name=self.football_config.england.premier_league.outright_market_name,
                                    start_time=start_time,
                                    cashout=cashout,
                                    is_live=is_live,
                                    is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event,
                                    event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_football_event_to_autotest_league2(self, markets=None, lp=None, cashout=True, start_time=None,
                                               is_live=False, is_upcoming=False, wait_for_event=True, **kwargs):
        return self.add_sport_event(markets=markets,
                                    class_id=self.football_config.autotest_class.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.autotest_class.autotest_league2.type_id,
                                    market_template_id=self.football_config.autotest_class.autotest_league2.market_template_id,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    lp=lp, start_time=start_time, wait_for_event=wait_for_event, **kwargs)

    def add_football_event_to_featured_autotest_league(self, markets=None, start_time=None,
                                                       wait_for_event=True, **kwargs):
        """
        Do not use this method for other purposes than Featured modules testing
        :param markets: markets
        :param start_time: start time
        :param wait_for_event: True or False
        :param kwargs: extra options
        :return: event params
        """
        return self.add_sport_event(markets=markets,
                                    class_id=self.football_config.autotest_class.class_id,
                                    category_id=self.football_config.category_id,
                                    type_id=self.football_config.autotest_class.featured_autotest_league.type_id,
                                    market_template_id=self.football_config.autotest_class.featured_autotest_league.market_template_id,
                                    start_time=start_time, wait_for_event=wait_for_event, **kwargs)

    def add_your_call_specials(self, cashout=True, start_time=None, is_live=False, is_upcoming=False,
                               markets=None, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.your_call_config.your_call_class.class_id,
                                    category_id=self.your_call_config.category_id,
                                    type_id=self.your_call_config.your_call_class.your_call_specials.type_id,
                                    market_template_id=self.your_call_config.your_call_class.your_call_specials.your_call_specials_market_template_id,
                                    default_market_name=self.your_call_config.your_call_class.your_call_specials.your_call_specials_market_name,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    markets=markets, start_time=start_time, wait_for_event=wait_for_event, **kwargs)

    def add_event_to_coupon(self, market_id, coupon_name, **kwargs):
        """
        :param market_id: market id of event that should be added to coupon
        :param coupon_name: one of 'Football Autotest Coupon', 'UK Coupon', 'Euro Elite Coupon', 'Televised Matches',
                'Football Auto Test Coupon No Cashout', 'Auto Hiding Test Coupon', 'Tennis Auto Test Coupon', 'Basketball Auto Test Coupon'
        :param kwargs: coupon_id : coupon id for sports except football
        :return: None
        """
        c = Coupon(env=self.env, brand=self.brand)
        coupon_id = kwargs.get('coupon_id', None)
        if coupon_id:
            c.add_market_to_coupon(coupon_id=coupon_id, market_id=market_id)
        else:
            c.add_market_to_coupon(coupon_id=self.football_config.coupons[coupon_name], market_id=market_id)

    def add_tennis_event_to_autotest_trophy(self, markets=None, cashout=True, is_off=None, is_upcoming=False,
                                            start_time=None, is_live=False, lp=None, wait_for_event=True,
                                            timeout=15, **kwargs):
        return self.add_sport_event(class_id=self.tennis_config.tennis_autotest.class_id,
                                    category_id=self.tennis_config.category_id,
                                    type_id=self.tennis_config.tennis_autotest.autotest_trophy.type_id,
                                    market_template_id=self.tennis_config.tennis_autotest.autotest_trophy.market_template_id,
                                    markets=markets,
                                    default_market_name=self.tennis_config.tennis_autotest.autotest_trophy.market_name,
                                    cashout=cashout, is_live=is_live, is_off=is_off, is_upcoming=is_upcoming,
                                    start_time=start_time, lp=lp, wait_for_event=wait_for_event, timeout=timeout,
                                    **kwargs)

    def add_tennis_event_to_davis_cup(self, markets=None, cashout=True, is_off=None, is_upcoming=False,
                                      start_time=None, is_live=False, lp=None, wait_for_event=True,
                                      timeout=15, **kwargs):
        return self.add_sport_event(class_id=self.tennis_config.tennis_all_tennis.class_id,
                                    category_id=self.tennis_config.category_id,
                                    type_id=self.tennis_config.tennis_all_tennis.davis_cup.type_id,
                                    market_template_id=self.tennis_config.tennis_all_tennis.davis_cup.market_template_id,
                                    markets=markets,
                                    default_market_name=self.tennis_config.tennis_all_tennis.davis_cup.market_name,
                                    cashout=cashout, is_live=is_live, is_off=is_off, is_upcoming=is_upcoming,
                                    start_time=start_time, lp=lp, wait_for_event=wait_for_event, timeout=timeout,
                                    **kwargs)

    def add_tennis_event_to_european_open(self, markets=None, cashout=True, is_off=None, is_upcoming=False,
                                          start_time=None, is_live=False, lp=None, wait_for_event=True,
                                          timeout=15, **kwargs):
        return self.add_sport_event(class_id=self.tennis_config.tennis_all_tennis.class_id,
                                    category_id=self.tennis_config.category_id,
                                    type_id=self.tennis_config.tennis_all_tennis.european_open.type_id,
                                    market_template_id=self.tennis_config.tennis_all_tennis.european_open.market_template_id,
                                    markets=markets,
                                    default_market_name=self.tennis_config.tennis_all_tennis.european_open.market_name,
                                    cashout=cashout, is_live=is_live, is_off=is_off, is_upcoming=is_upcoming,
                                    start_time=start_time, lp=lp, wait_for_event=wait_for_event, timeout=timeout,
                                    **kwargs)

    def add_tennis_event_to_nice_open(self, markets=None, cashout=True, is_off=None, is_upcoming=False,
                                      start_time=None, is_live=False, lp=None, wait_for_event=True,
                                      timeout=15, **kwargs):
        return self.add_sport_event(class_id=self.tennis_config.tennis_all_tennis.class_id,
                                    category_id=self.tennis_config.category_id,
                                    type_id=self.tennis_config.tennis_all_tennis.nice_open.type_id,
                                    market_template_id=self.tennis_config.tennis_all_tennis.nice_open.market_template_id,
                                    markets=markets,
                                    default_market_name=self.tennis_config.tennis_all_tennis.nice_open.market_name,
                                    cashout=cashout, is_live=is_live, is_off=is_off, is_upcoming=is_upcoming,
                                    start_time=start_time, lp=lp, wait_for_event=wait_for_event, timeout=timeout,
                                    **kwargs)

    def add_tennis_outright_event_to_autotest_league(self, lp=None, start_time=None, cashout=True,
                                                     is_live=False, is_upcoming=False, wait_for_event=True,
                                                     **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.tennis_config.tennis_autotest.class_id,
                                    category_id=self.tennis_config.category_id,
                                    type_id=self.tennis_config.tennis_autotest.autotest_trophy.type_id,
                                    market_template_id=self.tennis_config.tennis_autotest.autotest_trophy.outright_market_template_id,
                                    default_market_name=self.tennis_config.tennis_autotest.autotest_trophy.outright_market_name,
                                    lp=lp, start_time=start_time, cashout=cashout, is_live=is_live,
                                    is_upcoming=is_upcoming, wait_for_event=wait_for_event,
                                    event_name=event_name, sort=sort_type,
                                    **kwargs)

    def add_tennis_event_enhanced_multiples(self, start_time=None, is_live=False,
                                            selection_type='all to win in 90 Mins', wait_for_event=True):
        return self.add_sport_event(class_id=self.tennis_config.specials.class_id,
                                    category_id=self.tennis_config.category_id,
                                    type_id=self.tennis_config.specials.enhanced_multiples.type_id,
                                    market_template_id=self.tennis_config.specials.enhanced_multiples.market_template_id,
                                    default_market_name=self.tennis_config.specials.enhanced_multiples.market_name,
                                    start_time=start_time, is_live=is_live, selection_type=selection_type,
                                    wait_for_event=wait_for_event)

    def add_baseball_event_to_autotest_league(self, cashout=True, lp=None, is_live=False, start_time=None,
                                              is_upcoming=False, wait_for_event=True, timeout=15, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.baseball.category_id,
                                    class_id=self.backend.ti.baseball.baseball_autotest.class_id,
                                    type_id=self.backend.ti.baseball.baseball_autotest.autotest_league.type_id,
                                    market_template_id=self.backend.ti.baseball.baseball_autotest.autotest_league.market_template_id,
                                    default_market_name=self.backend.ti.baseball.baseball_autotest.autotest_league.market_name,
                                    cashout=cashout, is_live=is_live, lp=lp, start_time=start_time, timeout=timeout,
                                    is_upcoming=is_upcoming, wait_for_event=wait_for_event, **kwargs)

    def add_baseball_event_to_autotest_handicap(self, cashout=True, lp=None, is_live=False, start_time=None,
                                              is_upcoming=False, wait_for_event=True, timeout=15, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.baseball.category_id,
                                    class_id=self.backend.ti.baseball.baseball_autotest.class_id,
                                    type_id=self.backend.ti.baseball.baseball_autotest.autotest_handicap.type_id,
                                    market_template_id=self.backend.ti.baseball.baseball_autotest.autotest_handicap.market_template_id,
                                    default_market_name=self.backend.ti.baseball.baseball_autotest.autotest_handicap.market_name,
                                    cashout=cashout, is_live=is_live, lp=lp, start_time=start_time, timeout=timeout,
                                    is_upcoming=is_upcoming, wait_for_event=wait_for_event, **kwargs)

    def add_baseball_event_to_us_league(self, cashout=True, is_live=False, is_upcoming=False, wait_for_event=True,
                                        **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.baseball.category_id,
                                    class_id=self.backend.ti.baseball.us_baseball.class_id,
                                    type_id=self.backend.ti.baseball.us_baseball.mlb.type_id,
                                    market_template_id=self.backend.ti.baseball.us_baseball.mlb.market_template_id,
                                    default_market_name=self.backend.ti.baseball.us_baseball.mlb.market_name,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_baseball_event_to_germany_league(self, cashout=True, is_live=False, is_upcoming=False, wait_for_event=True,
                                             **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.baseball.category_id,
                                    class_id=self.backend.ti.baseball.german_baseball.class_id,
                                    type_id=self.backend.ti.baseball.german_baseball.bundesliga_nord.type_id,
                                    market_template_id=self.backend.ti.baseball.german_baseball.bundesliga_nord.market_template_id,
                                    default_market_name=self.backend.ti.baseball.german_baseball.bundesliga_nord.market_name,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_baseball_event_to_world_league(self, cashout=True, is_live=False, is_upcoming=False, wait_for_event=True,
                                           **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.baseball.category_id,
                                    class_id=self.backend.ti.baseball.international_baseball.class_id,
                                    type_id=self.backend.ti.baseball.international_baseball.world.type_id,
                                    market_template_id=self.backend.ti.baseball.international_baseball.world.market_template_id,
                                    default_market_name=self.backend.ti.baseball.international_baseball.world.market_name,
                                    cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_american_football_event_to_autotest_league(self, lp=None, start_time=None, is_live=False, is_upcoming=False,
                                                       timeout=15, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.backend.ti.american_football.american_football_autotest.class_id,
                                    category_id=self.backend.ti.american_football.category_id,
                                    type_id=self.backend.ti.american_football.american_football_autotest.autotest_league.type_id,
                                    market_template_id=self.backend.ti.american_football.american_football_autotest.autotest_league.market_template_id,
                                    default_market_name=self.backend.ti.american_football.american_football_autotest.autotest_league.market_name,
                                    lp=lp, start_time=start_time, is_live=is_live, is_upcoming=is_upcoming,
                                    timeout=timeout, wait_for_event=wait_for_event, **kwargs)

    def add_american_football_event_to_autotest_handicap(self, lp=None, start_time=None, is_live=False, is_upcoming=False,
                                                        timeout=15, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.backend.ti.american_football.american_football_autotest.class_id,
                                    category_id=self.backend.ti.american_football.category_id,
                                    type_id=self.backend.ti.american_football.american_football_autotest.american_football_autotest_handicap.type_id,
                                    market_template_id=self.backend.ti.american_football.american_football_autotest.american_football_autotest_handicap.market_template_id,
                                    default_market_name=self.backend.ti.american_football.american_football_autotest.american_football_autotest_handicap.market_name,
                                    lp=lp, start_time=start_time, is_live=is_live, is_upcoming=is_upcoming,
                                    timeout=timeout, wait_for_event=wait_for_event, **kwargs)

    def add_american_football_outright_event_to_autotest_league(self, lp=None, start_time=None,
                                                                cashout=True,
                                                                is_live=False, is_upcoming=False, wait_for_event=True,
                                                                **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.backend.ti.american_football.american_football_autotest.class_id,
                                    category_id=self.backend.ti.american_football.category_id,
                                    type_id=self.backend.ti.american_football.american_football_autotest.autotest_league.type_id,
                                    market_template_id=self.backend.ti.american_football.american_football_autotest.autotest_league.outright_id,
                                    default_market_name=self.backend.ti.american_football.american_football_autotest.autotest_league.outright_name,
                                    lp=lp, start_time=start_time, cashout=cashout, is_live=is_live,
                                    is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, event_name=event_name, sort=sort_type, **kwargs)

    def add_american_football_event_to_nfl(self, cashout=True, wait_for_event=True, is_live=False, **kwargs):
        return self.add_sport_event(class_id=self.backend.ti.american_football.american_football_usa.class_id,
                                    category_id=self.backend.ti.american_football.category_id,
                                    type_id=self.backend.ti.american_football.american_football_usa.nfl.type_id,
                                    market_template_id=self.backend.ti.american_football.american_football_usa.nfl.market_template_id,
                                    default_market_name=self.backend.ti.american_football.american_football_usa.nfl.market_name,
                                    cashout=cashout, wait_for_event=wait_for_event, is_live=is_live, **kwargs)

    def add_american_football_event_to_ncaa_bowls(self, cashout=True, wait_for_event=True, is_live=False, **kwargs):
        return self.add_sport_event(class_id=self.backend.ti.american_football.american_football_usa.class_id,
                                    category_id=self.backend.ti.american_football.category_id,
                                    type_id=self.backend.ti.american_football.american_football_usa.ncaa_bowls.type_id,
                                    market_template_id=self.backend.ti.american_football.american_football_usa.ncaa_bowls.market_template_id,
                                    default_market_name=self.backend.ti.american_football.american_football_usa.ncaa_bowls.market_name,
                                    cashout=cashout, wait_for_event=wait_for_event, is_live=is_live, **kwargs)

    def add_american_football_event_to_cfl(self, cashout=True, wait_for_event=True, is_live=False, **kwargs):
        return self.add_sport_event(class_id=self.backend.ti.american_football.american_football_canada.class_id,
                                    category_id=self.backend.ti.american_football.category_id,
                                    type_id=self.backend.ti.american_football.american_football_canada.cfl.type_id,
                                    market_template_id=self.backend.ti.american_football.american_football_canada.cfl.market_template_id,
                                    default_market_name=self.backend.ti.american_football.american_football_canada.cfl.market_name,
                                    cashout=cashout, wait_for_event=wait_for_event, is_live=is_live, **kwargs)

    def add_basketball_event_to_austrian_league(self, start_time=None, cashout=True, is_live=False, wait_for_event=True,
                                                **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.basketball.category_id,
                                    class_id=self.backend.ti.basketball.basketball_austria.class_id,
                                    type_id=self.backend.ti.basketball.basketball_austria.abl.type_id,
                                    market_template_id=self.backend.ti.basketball.basketball_austria.abl.market_template_id,
                                    default_market_name=self.backend.ti.basketball.basketball_austria.abl.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_basketball_event_to_basketball_autotest_handicap(self, start_time=None, cashout=True, is_live=False,
                                                             wait_for_event=True,
                                                             **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.basketball.category_id,
                                    class_id=self.backend.ti.basketball.basketball_autotest.class_id,
                                    type_id=self.backend.ti.basketball.basketball_autotest.basketball_autotest_total_points.type_id,
                                    market_template_id=self.backend.ti.basketball.basketball_autotest.basketball_autotest_total_points.market_template_id,
                                    default_market_name=self.backend.ti.basketball.basketball_autotest.basketball_autotest_total_points.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_basketball_event_to_croatian_league(self, start_time=None, cashout=True, is_live=False, wait_for_event=True,
                                                **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.basketball.category_id,
                                    class_id=self.backend.ti.basketball.basketball_croatia.class_id,
                                    type_id=self.backend.ti.basketball.basketball_croatia.croatia_cup.type_id,
                                    market_template_id=self.backend.ti.basketball.basketball_croatia.croatia_cup.market_template_id,
                                    default_market_name=self.backend.ti.basketball.basketball_croatia.croatia_cup.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_basketball_event_to_autotest_league(self, start_time=None, cashout=True, is_live=False, lp=None,
                                                is_off=None, is_upcoming=False, wait_for_event=True, timeout=15):
        return self.add_sport_event(category_id=self.backend.ti.basketball.category_id,
                                    class_id=self.backend.ti.basketball.basketball_autotest.class_id,
                                    type_id=self.backend.ti.basketball.basketball_autotest.autotest_league.type_id,
                                    market_template_id=self.backend.ti.basketball.basketball_autotest.autotest_league.market_template_id,
                                    default_market_name=self.backend.ti.basketball.basketball_autotest.autotest_league.market_name,
                                    start_time=start_time, cashout=cashout, lp=lp, is_live=is_live, is_off=is_off,
                                    is_upcoming=is_upcoming, wait_for_event=wait_for_event, timeout=timeout)

    def add_basketball_outright_event_to_autotest_league(self, start_time=None, markets=None, cashout=True,
                                                         is_live=False, is_upcoming=False, wait_for_event=True,
                                                         **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.backend.ti.basketball.basketball_autotest.class_id,
                                    category_id=self.backend.ti.basketball.category_id,
                                    type_id=self.backend.ti.basketball.basketball_autotest.autotest_league.type_id,
                                    markets=markets,
                                    market_template_id=self.backend.ti.basketball.basketball_autotest.autotest_league.outright_market_template_id,
                                    default_market_name=self.backend.ti.basketball.basketball_autotest.autotest_league.outright_market_name,
                                    start_time=start_time, cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, event_name=event_name, sort=sort_type, **kwargs)

    def add_basketball_event_to_us_league(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.basketball.category_id,
                                    class_id=self.backend.ti.basketball.basketball_usa.class_id,
                                    type_id=self.backend.ti.basketball.basketball_usa.nba.type_id,
                                    market_template_id=self.backend.ti.basketball.basketball_usa.nba.market_template_id,
                                    default_market_name=self.backend.ti.basketball.basketball_usa.nba.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_basketball_event_enhanced_multiples(self, start_time=None, is_live=False,
                                                selection_type='all to win in 90 Mins', wait_for_event=True):
        return self.add_sport_event(class_id=self.basketball_config.specials.class_id,
                                    category_id=self.basketball_config.category_id,
                                    type_id=self.basketball_config.specials.enhanced_multiples.type_id,
                                    market_template_id=self.basketball_config.specials.enhanced_multiples.market_template_id,
                                    default_market_name=self.basketball_config.specials.enhanced_multiples.market_name,
                                    start_time=start_time, is_live=is_live, selection_type=selection_type,
                                    wait_for_event=wait_for_event)

    def add_volleyball_event_to_austrian_league(self, start_time=None, cashout=True, is_live=False, wait_for_event=True,
                                                **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.volleyball.category_id,
                                    class_id=self.backend.ti.volleyball.volleyball_austria.class_id,
                                    type_id=self.backend.ti.volleyball.volleyball_austria.avl.type_id,
                                    market_template_id=self.backend.ti.volleyball.volleyball_austria.avl.market_template_id,
                                    default_market_name=self.backend.ti.volleyball.volleyball_austria.avl.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_volleyball_event_to_austrian_league_avl_set_handicap(self, start_time=None, cashout=True, is_live=False, wait_for_event=True,
                                                **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.volleyball.category_id,
                                    class_id=self.backend.ti.volleyball.volleyball_austria.class_id,
                                    type_id=self.backend.ti.volleyball.volleyball_austria.avl_set_handicap.type_id,
                                    market_template_id=self.backend.ti.volleyball.volleyball_austria.avl_set_handicap.market_template_id,
                                    default_market_name=self.backend.ti.volleyball.volleyball_austria.avl_set_handicap.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_beach_volleyball_event_to_austrian_cup(self, start_time=None, cashout=True, is_live=False,
                                                   wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.beach_volleyball.category_id,
                                    class_id=self.backend.ti.beach_volleyball.beach_volleyball_austria.class_id,
                                    type_id=self.backend.ti.beach_volleyball.beach_volleyball_austria.austrian_cup_womans.type_id,
                                    market_template_id=self.backend.ti.beach_volleyball.beach_volleyball_austria.austrian_cup_womans.market_template_id,
                                    default_market_name=self.backend.ti.beach_volleyball.beach_volleyball_austria.austrian_cup_womans.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_handball_event_to_croatian_premijer_liga(self, start_time=None, cashout=True, is_live=False,
                                                     wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.handball.category_id,
                                    class_id=self.backend.ti.handball.handball_croatia.class_id,
                                    type_id=self.backend.ti.handball.handball_croatia.dukat_premijer_liga.type_id,
                                    market_template_id=self.backend.ti.handball.handball_croatia.dukat_premijer_liga.market_template_id,
                                    default_market_name=self.backend.ti.handball.handball_croatia.dukat_premijer_liga.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_darts_event_to_darts_all_darts(self, start_time=None, cashout=True, is_live=False, markets=None,
                                                             wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.darts.category_id,
                                    class_id=self.backend.ti.darts.darts_autotest.class_id,
                                    type_id=self.backend.ti.darts.darts_autotest.championship_league.type_id,
                                    markets=markets,
                                    default_market_name=self.backend.ti.darts.darts_autotest.championship_league.market_name,
                                    market_template_id=self.backend.ti.darts.darts_autotest.championship_league.market_template_id,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_darts_event_for_WW_type(self, start_time=None, cashout=True, is_live=False, wait_for_event=True,
                                               **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.darts.category_id,
                                    class_id=self.backend.ti.darts.darts_autotest.class_id,
                                    type_id=self.backend.ti.darts.darts_autotest.darts_autotest_ww.type_id,
                                    market_template_id=self.backend.ti.darts.darts_autotest.darts_autotest_ww.market_template_id,
                                    default_market_name=self.backend.ti.darts.darts_autotest.darts_autotest_ww.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_darts_event_for_handicap(self, start_time=None, cashout=True, is_live=False, wait_for_event=True,
                                              **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.darts.category_id,
                                    class_id=self.backend.ti.darts.darts_autotest.class_id,
                                    type_id=self.backend.ti.darts.darts_autotest.darts_autotest_handicap.type_id,
                                    market_template_id=self.backend.ti.darts.darts_autotest.darts_autotest_handicap.market_template_id,
                                    default_market_name=self.backend.ti.darts.darts_autotest.darts_autotest_handicap.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_boxing_event(self, start_time=None, cashout=True, is_live=False, markets=None,
                                  wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.boxing.category_id,
                                    class_id=self.backend.ti.boxing.boxing_all_boxing.class_id,
                                    type_id=self.backend.ti.boxing.boxing_all_boxing.autotest_boxing.type_id,
                                    markets=markets,
                                    market_template_id=self.backend.ti.boxing.boxing_all_boxing.autotest_boxing.market_template_id,
                                    default_market_name=self.backend.ti.boxing.boxing_all_boxing.autotest_boxing.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_badminton_event_to_autotest_league(self, start_time=None, cashout=True, is_live=False,
                                                wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.badminton.category_id,
                                    class_id=self.backend.ti.badminton.badminton_autotest.class_id,
                                    type_id=self.backend.ti.badminton.badminton_autotest.autotest_league.type_id,
                                    market_template_id=self.backend.ti.badminton.badminton_autotest.autotest_league.market_template_id,
                                    default_market_name=self.backend.ti.badminton.badminton_autotest.autotest_league.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_cricket_event(self, start_time=None, cashout=True, is_live=False,
                                                wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.cricket.category_id,
                                    class_id=self.backend.ti.cricket.cricket_all_cricket.class_id,
                                    type_id=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest.type_id,
                                    market_template_id=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest.market_template_id,
                                    default_market_name=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_cricket_event_with_total_sixes(self, start_time=None, cashout=True, is_live=False,
                                                               wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.cricket.category_id,
                                    class_id=self.backend.ti.cricket.cricket_all_cricket.class_id,
                                    type_id=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest_total_sixes.type_id,
                                    market_template_id=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest_total_sixes.market_template_id,
                                    default_market_name=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest_total_sixes.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_cricket_event_for_WW_type(self, start_time=None, cashout=True, is_live=False,
                                               wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.cricket.category_id,
                                    class_id=self.backend.ti.cricket.cricket_all_cricket.class_id,
                                    type_id=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest_ww.type_id,
                                    market_template_id=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest_ww.market_template_id,
                                    default_market_name=self.backend.ti.cricket.cricket_all_cricket.cricket_autotest_ww.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_UK_racing_event(self, number_of_runners=5, markets=None, cashout=True, ew_terms=None, lp_prices=None,
                            wait_for_event=True, is_tomorrow=False, is_live=False, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.horse_racing_live.class_id,
                                     type_id=self.horseracing_config.horse_racing_live.autotest_uk.type_id,
                                     default_market_name=self.horseracing_config.horse_racing_live.autotest_uk.market_name,
                                     market_template_id=self.horseracing_config.horse_racing_live.autotest_uk.market_template_id,
                                     event_name_pattern=self.horseracing_config.horse_racing_live.autotest_uk.name_pattern,
                                     markets=markets, cashout=cashout, ew_terms=ew_terms,
                                     number_of_runners=number_of_runners,
                                     is_tomorrow=is_tomorrow, is_live=is_live, lp_prices=lp_prices,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_UK_greyhound_racing_event(self, number_of_runners=5, cashout=True, lp_prices=None, ew_terms=None,
                                      forecast_available=False, tricast_available=False, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.backend.ti.greyhound_racing.category_id,
                                     class_id=self.backend.ti.greyhound_racing.greyhounds_live.class_id,
                                     type_id=self.backend.ti.greyhound_racing.greyhounds_live.autotest.type_id,
                                     market_template_id=self.backend.ti.greyhound_racing.greyhounds_live.autotest.market_template_id,
                                     default_market_name=self.backend.ti.greyhound_racing.greyhounds_live.autotest.market_name,
                                     event_name_pattern=self.backend.ti.greyhound_racing.greyhounds_live.autotest.name_pattern,
                                     number_of_runners=number_of_runners, cashout=cashout, lp_prices=lp_prices,
                                     ew_terms=ew_terms, forecast_available=forecast_available,
                                     tricast_available=tricast_available, wait_for_event=wait_for_event, **kwargs)

    def add_international_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.horse_racing_live.class_id,
                                     type_id=self.horseracing_config.horse_racing_live.autotest_international.type_id,
                                     event_name_pattern=self.horseracing_config.horse_racing_live.autotest_international.name_pattern,
                                     market_template_id=self.horseracing_config.horse_racing_live.autotest_international.market_template_id,
                                     default_market_name=self.horseracing_config.horse_racing_live.autotest_international.market_name,
                                     cashout=cashout, number_of_runners=number_of_runners,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_irish_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.horse_racing_live.class_id,
                                     type_id=self.horseracing_config.horse_racing_live.autotest_ireland.type_id,
                                     event_name_pattern=self.horseracing_config.horse_racing_live.autotest_ireland.name_pattern,
                                     market_template_id=self.horseracing_config.horse_racing_live.autotest_ireland.market_template_id,
                                     default_market_name=self.horseracing_config.horse_racing_live.autotest_ireland.market_name,
                                     cashout=cashout, number_of_runners=number_of_runners,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_virtual_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.horse_racing_live.class_id,
                                     type_id=self.horseracing_config.horse_racing_live.autotest_virtual.type_id,
                                     event_name_pattern=self.horseracing_config.horse_racing_live.autotest_virtual.name_pattern,
                                     market_template_id=self.horseracing_config.horse_racing_live.autotest_virtual.market_template_id,
                                     default_market_name=self.horseracing_config.horse_racing_live.autotest_virtual.market_name,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_virtual_greyhound_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.backend.ti.greyhound_racing.category_id,
                                     class_id=self.backend.ti.greyhound_racing.greyhounds_live.class_id,
                                     type_id=self.backend.ti.greyhound_racing.greyhounds_live.autotest_virtual.type_id,
                                     event_name_pattern=self.backend.ti.greyhound_racing.greyhounds_live.autotest_virtual.name_pattern,
                                     market_template_id=self.backend.ti.greyhound_racing.greyhounds_live.autotest_virtual.market_template_id,
                                     default_market_name=self.backend.ti.greyhound_racing.greyhounds_live.autotest_virtual.market_name,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_winning_distance_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.daily_racing_specials.class_id,
                                     type_id=self.horseracing_config.daily_racing_specials.winning_distances.type_id,
                                     event_name_pattern=self.horseracing_config.daily_racing_specials.winning_distances.name_pattern,
                                     default_market_name=self.horseracing_config.daily_racing_specials.winning_distances.market_name,
                                     market_template_id=self.horseracing_config.daily_racing_specials.winning_distances.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_price_bomb_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.daily_racing_specials.class_id,
                                     type_id=self.horseracing_config.daily_racing_specials.price_bomb.type_id,
                                     event_name_pattern=self.horseracing_config.daily_racing_specials.price_bomb.name_pattern,
                                     default_market_name=self.horseracing_config.daily_racing_specials.price_bomb.market_name,
                                     market_template_id=self.horseracing_config.daily_racing_specials.price_bomb.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_enhanced_multiples_racing_event(self, number_of_runners=1, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.daily_racing_specials.class_id,
                                     type_id=self.horseracing_config.daily_racing_specials.enhanced_multiples.type_id,
                                     event_name_pattern=self.horseracing_config.daily_racing_specials.enhanced_multiples.name_pattern,
                                     default_market_name=self.horseracing_config.daily_racing_specials.enhanced_multiples.market_name,
                                     market_template_id=self.horseracing_config.daily_racing_specials.enhanced_multiples.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_mobile_exclusive_racing_event(self, number_of_runners=5, cashout=True, wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.daily_racing_specials.class_id,
                                     type_id=self.horseracing_config.daily_racing_specials.mobile_exclusive.type_id,
                                     event_name_pattern=self.horseracing_config.daily_racing_specials.mobile_exclusive.name_pattern,
                                     default_market_name=self.horseracing_config.daily_racing_specials.mobile_exclusive.market_name,
                                     market_template_id=self.horseracing_config.daily_racing_specials.mobile_exclusive.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_racing_your_call_specials_event(self, number_of_runners=5, cashout=True, wait_for_event=True, lp_prices=None, **kwargs):
        default_market_name = kwargs.pop('default_market_name',
                                         self.horseracing_config.daily_racing_specials.your_call_specials.market_name)
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.daily_racing_specials.class_id,
                                     type_id=self.horseracing_config.daily_racing_specials.your_call_specials.type_id,
                                     event_name_pattern=self.horseracing_config.daily_racing_specials.your_call_specials.name_pattern,
                                     default_market_name=default_market_name,
                                     market_template_id=self.horseracing_config.daily_racing_specials.your_call_specials.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout,
                                     lp_prices=lp_prices, wait_for_event=wait_for_event, **kwargs)

    def add_racing_specials_event(self, number_of_runners=5, cashout=True, ew_terms=None, specials=True, lp_prices=None,
                                  wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.horseracing_config.category_id,
                                     class_id=self.horseracing_config.horse_racing_specials.class_id,
                                     type_id=self.horseracing_config.horse_racing_specials.racing_specials.type_id,
                                     event_name_pattern=self.horseracing_config.horse_racing_specials.racing_specials.name_pattern,
                                     default_market_name=self.horseracing_config.horse_racing_specials.racing_specials.market_name,
                                     market_template_id=self.horseracing_config.horse_racing_specials.racing_specials.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout, ew_terms=ew_terms,
                                     specials=specials, lp_prices=lp_prices,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_greyhound_racing_specials_event(self, number_of_runners=5, cashout=True, ew_terms=None, specials=True, lp_prices=None,
                                  wait_for_event=True, **kwargs):
        return self.add_racing_event(category_id=self.greyhound_racing_config.category_id,
                                     class_id=self.greyhound_racing_config.greyhound_racing_specials.class_id,
                                     type_id=self.greyhound_racing_config.greyhound_racing_specials.racing_specials.type_id,
                                     event_name_pattern=self.greyhound_racing_config.greyhound_racing_specials.racing_specials.name_pattern,
                                     default_market_name=self.greyhound_racing_config.greyhound_racing_specials.racing_specials.market_name,
                                     market_template_id=self.greyhound_racing_config.greyhound_racing_specials.racing_specials.market_template_id,
                                     number_of_runners=number_of_runners, cashout=cashout, ew_terms=ew_terms,
                                     specials=specials, lp_prices=lp_prices,
                                     wait_for_event=wait_for_event, **kwargs)

    def add_motor_bikes_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Moto Bike Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.motor_bikes.category_id,
                                    class_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.class_id,
                                    type_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.british_125cc_gp.type_id,
                                    market_template_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.british_125cc_gp.market_template_id,
                                    default_market_name=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.british_125cc_gp.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_motor_bikes_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.motor_bikes.category_id,
                                    class_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.class_id,
                                    type_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.british_125cc_gp.type_id,
                                    market_template_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.british_125cc_gp.outright_market_template_id,
                                    default_market_name=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.british_125cc_gp.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_motor_bikes_world_superbikesbrno_gp_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.motor_bikes.category_id,
                                    class_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.class_id,
                                    type_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikesbrno_gp.type_id,
                                    market_template_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikesbrno_gp.outright_market_template_id,
                                    default_market_name=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikesbrno_gp.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_motor_bikes_world_superbikes_championship_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.motor_bikes.category_id,
                                    class_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.class_id,
                                    type_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikes_championship.type_id,
                                    market_template_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikes_championship.outright_market_template_id,
                                    default_market_name=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikes_championship.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_motor_bikes_world_superbikes_philip_island_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.motor_bikes.category_id,
                                    class_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.class_id,
                                    type_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikes_philip_island.type_id,
                                    market_template_id=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikes_philip_island.outright_market_template_id,
                                    default_market_name=self.backend.ti.motor_bikes.motor_bikes_all_motor_bikes.world_superbikes_philip_island.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_formula_1_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Formula 1 Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.formula_1.category_id,
                                    class_id=self.backend.ti.formula_1.formula_1_all_f1.class_id,
                                    type_id=self.backend.ti.formula_1.formula_1_all_f1.world_championship.type_id,
                                    market_template_id=self.backend.ti.formula_1.formula_1_all_f1.world_championship.market_template_id,
                                    default_market_name=self.backend.ti.formula_1.formula_1_all_f1.world_championship.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_formula_1_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright Formula 1 Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.formula_1.category_id,
                                    class_id=self.backend.ti.formula_1.formula_1_all_f1.class_id,
                                    type_id=self.backend.ti.formula_1.formula_1_all_f1.world_championship.type_id,
                                    market_template_id=self.backend.ti.formula_1.formula_1_all_f1.world_championship.outright_market_template_id,
                                    default_market_name=self.backend.ti.formula_1.formula_1_all_f1.world_championship.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_formula_1_british_grand_prix_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright Formula 1 Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.formula_1.category_id,
                                    class_id=self.backend.ti.formula_1.formula_1_all_f1.class_id,
                                    type_id=self.backend.ti.formula_1.formula_1_all_f1.british_grand_prix.type_id,
                                    market_template_id=self.backend.ti.formula_1.formula_1_all_f1.british_grand_prix.outright_market_template_id,
                                    default_market_name=self.backend.ti.formula_1.formula_1_all_f1.british_grand_prix.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_formula_1_indian_grand_prix_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright Formula 1 Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.formula_1.category_id,
                                    class_id=self.backend.ti.formula_1.formula_1_all_f1.class_id,
                                    type_id=self.backend.ti.formula_1.formula_1_all_f1.indian_grand_prix.type_id,
                                    market_template_id=self.backend.ti.formula_1.formula_1_all_f1.indian_grand_prix.outright_market_template_id,
                                    default_market_name=self.backend.ti.formula_1.formula_1_all_f1.indian_grand_prix.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_formula_1_european_grand_prix_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright Formula 1 Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.formula_1.category_id,
                                    class_id=self.backend.ti.formula_1.formula_1_all_f1.class_id,
                                    type_id=self.backend.ti.formula_1.formula_1_all_f1.european_grand_prix.type_id,
                                    market_template_id=self.backend.ti.formula_1.formula_1_all_f1.european_grand_prix.outright_market_template_id,
                                    default_market_name=self.backend.ti.formula_1.formula_1_all_f1.european_grand_prix.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_formula_1_united_states_grand_prix_outright_event(self, start_time=None, cashout=True, is_live=False, wait_for_event=True, **kwargs):
        event_name = kwargs.pop('event_name', 'Outright Formula 1 Event %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(category_id=self.backend.ti.formula_1.category_id,
                                    class_id=self.backend.ti.formula_1.formula_1_all_f1.class_id,
                                    type_id=self.backend.ti.formula_1.formula_1_all_f1.united_states_grand_prix.type_id,
                                    market_template_id=self.backend.ti.formula_1.formula_1_all_f1.united_states_grand_prix.outright_market_template_id,
                                    default_market_name=self.backend.ti.formula_1.formula_1_all_f1.united_states_grand_prix.outright_market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_gaelic_football_event_to_gaelic_football_all_gaelic_football(self, start_time=None, cashout=True,
                                                                         is_live=False,
                                                                         wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.gaelic_football.category_id,
                                    class_id=self.backend.ti.gaelic_football.gaelic_football_all_gaelic_football.class_id,
                                    type_id=self.backend.ti.gaelic_football.gaelic_football_all_gaelic_football.club_football.type_id,
                                    market_template_id=self.backend.ti.gaelic_football.gaelic_football_all_gaelic_football.club_football.market_template_id,
                                    default_market_name=self.backend.ti.gaelic_football.gaelic_football_all_gaelic_football.club_football.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_rugby_union_event_to_rugby_union_all_rugby_union(self, start_time=None, cashout=True, is_live=False, markets=None,
                                                             wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.rugby_union.category_id,
                                    class_id=self.backend.ti.rugby_union.rugby_union_all_rugby_union.class_id,
                                    type_id=self.backend.ti.rugby_union.rugby_union_all_rugby_union.world_cup.type_id,
                                    market_template_id=self.backend.ti.rugby_union.rugby_union_all_rugby_union.world_cup.market_template_id,
                                    default_market_name=self.backend.ti.rugby_union.rugby_union_all_rugby_union.world_cup.market_name,
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_rugby_union_event_to_rugby_autotest_handicap(self, start_time=None, cashout=True, is_live=False, markets=None,
                                                                wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.rugby_union.category_id,
                                    class_id=self.backend.ti.rugby_union.rugby_union_all_rugby_union.class_id,
                                    type_id=self.backend.ti.rugby_union.rugby_union_all_rugby_union.rugby_autotest_handicap.type_id,
                                    market_template_id=self.backend.ti.rugby_union.rugby_union_all_rugby_union.rugby_autotest_handicap.market_template_id,
                                    default_market_name=self.backend.ti.rugby_union.rugby_union_all_rugby_union.rugby_autotest_handicap.market_name,
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_snooker_event_to_snooker_all_snooker(self, start_time=None, cashout=True,
                                                 is_live=False,
                                                 wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.snooker.category_id,
                                    class_id=self.backend.ti.snooker.snooker_all_snooker.class_id,
                                    type_id=self.backend.ti.snooker.snooker_all_snooker.world_championship.type_id,
                                    market_template_id=self.backend.ti.snooker.snooker_all_snooker.world_championship.market_template_id,
                                    default_market_name=self.backend.ti.snooker.snooker_all_snooker.world_championship.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_rugby_league_event_to_rugby_league_all_rugby_league(self, start_time=None, cashout=True, is_live=False, markets=None,
                                                                wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.rugby_league.category_id,
                                    class_id=self.backend.ti.rugby_league.rugby_league_all_rugby_league.class_id,
                                    type_id=self.backend.ti.rugby_league.rugby_league_all_rugby_league.super_league.type_id,
                                    market_template_id=self.backend.ti.rugby_league.rugby_league_all_rugby_league.super_league.market_template_id,
                                    default_market_name=self.backend.ti.rugby_league.rugby_league_all_rugby_league.super_league.market_name,
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_rugby_league_event_to_rugby_autotest_handicap(self, start_time=None, cashout=True, is_live=False, markets=None,
                                                                wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.rugby_league.category_id,
                                    class_id=self.backend.ti.rugby_league.rugby_league_all_rugby_league.class_id,
                                    type_id=self.backend.ti.rugby_league.rugby_league_all_rugby_league.rugby_autotest_handicap.type_id,
                                    market_template_id=self.backend.ti.rugby_league.rugby_league_all_rugby_league.rugby_autotest_handicap.market_template_id,
                                    default_market_name=self.backend.ti.rugby_league.rugby_league_all_rugby_league.rugby_autotest_handicap.market_name,
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_hockey_event_to_super_league(self, start_time=None, cashout=True, is_live=False,
                                         wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.hockey.category_id,
                                    class_id=self.backend.ti.hockey.hockey_all_hockey.class_id,
                                    type_id=self.backend.ti.hockey.hockey_all_hockey.super_league.type_id,
                                    market_template_id=self.backend.ti.hockey.hockey_all_hockey.super_league.market_template_id,
                                    default_market_name=self.backend.ti.hockey.hockey_all_hockey.super_league.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_hockey_event_to_mens_olympics(self, start_time=None, cashout=True, is_live=False,
                                          wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.hockey.category_id,
                                    class_id=self.backend.ti.hockey.hockey_all_hockey.class_id,
                                    type_id=self.backend.ti.hockey.hockey_all_hockey.mens_olympics.type_id,
                                    market_template_id=self.backend.ti.hockey.hockey_all_hockey.mens_olympics.market_template_id,
                                    default_market_name=self.backend.ti.hockey.hockey_all_hockey.mens_olympics.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_hockey_event_to_olympics_specials(self, start_time=None, cashout=True, is_live=False,
                                              wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.hockey.category_id,
                                    class_id=self.backend.ti.hockey.hockey_all_hockey.class_id,
                                    type_id=self.backend.ti.hockey.hockey_all_hockey.olympics_specials.type_id,
                                    market_template_id=self.backend.ti.hockey.hockey_all_hockey.olympics_specials.market_template_id,
                                    default_market_name=self.backend.ti.hockey.hockey_all_hockey.olympics_specials.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_hockey_event_to_womens_olympics(self, start_time=None, cashout=True, is_live=False,
                                            wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.hockey.category_id,
                                    class_id=self.backend.ti.hockey.hockey_all_hockey.class_id,
                                    type_id=self.backend.ti.hockey.hockey_all_hockey.womens_olympics.type_id,
                                    market_template_id=self.backend.ti.hockey.hockey_all_hockey.womens_olympics.market_template_id,
                                    default_market_name=self.backend.ti.hockey.hockey_all_hockey.womens_olympics.market_name,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_hockey_event_outright_event(self, start_time=None, markets=None, cashout=True,
                                        is_live=False, is_upcoming=False, wait_for_event=True,
                                        **kwargs):
        event_name = kwargs.pop('event_name', 'Outright %s' % generate_name())
        sort_type = kwargs.pop('sort', 'TNMT')
        return self.add_sport_event(class_id=self.backend.ti.hockey.hockey_all_hockey.class_id,
                                    category_id=self.backend.ti.hockey.category_id,
                                    type_id=self.backend.ti.hockey.hockey_all_hockey.super_league.type_id,
                                    markets=markets,
                                    market_template_id=self.backend.ti.hockey.hockey_all_hockey.super_league.outright_market_template_id,
                                    default_market_name=self.backend.ti.hockey.hockey_all_hockey.super_league.outright_market_name,
                                    start_time=start_time,
                                    cashout=cashout,
                                    is_live=is_live,
                                    is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event,
                                    event_name=event_name,
                                    sort=sort_type,
                                    **kwargs)

    def add_ice_hockey_event_to_ice_hockey_usa(self, start_time=None, cashout=True, is_live=False, markets=None,
                                               wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.ice_hockey.category_id,
                                    class_id=self.backend.ti.ice_hockey.ice_hockey_usa.class_id,
                                    type_id=self.backend.ti.ice_hockey.ice_hockey_usa.ahl.type_id,
                                    market_template_id=self.backend.ti.ice_hockey.ice_hockey_usa.ahl.market_template_id,
                                    default_market_name=self.backend.ti.ice_hockey.ice_hockey_usa.ahl.market_name,
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_ice_hockey_event_to_ice_hockey_autotest_handicap(self, start_time=None, cashout=True, is_live=False,
                                                             markets=None, wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.ice_hockey.category_id,
                                    class_id=self.backend.ti.ice_hockey.ice_hockey_usa.class_id,
                                    type_id=self.backend.ti.ice_hockey.ice_hockey_usa.icehockey_autotest_handicap.type_id,
                                    market_template_id=self.backend.ti.ice_hockey.ice_hockey_usa.icehockey_autotest_handicap.market_template_id,
                                    default_market_name=self.backend.ti.ice_hockey.ice_hockey_usa.icehockey_autotest_handicap.market_name,
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_golf_event_to_golf_all_golf(self, start_time=None, cashout=True, is_live=False, markets=None,
                                               wait_for_event=True, **kwargs):
        return self.add_sport_event(category_id=self.backend.ti.golf.category_id,
                                    class_id=self.backend.ti.golf.golf_all_golf.class_id,
                                    type_id=self.backend.ti.golf.golf_all_golf.allianz_championship.type_id,
                                    market_template_id=kwargs.get('default_market_template_id', self.backend.ti.golf.golf_all_golf.allianz_championship.market_template_id),
                                    default_market_name=kwargs.get('default_market', self.backend.ti.golf.golf_all_golf.allianz_championship.market_name),
                                    markets=markets,
                                    cashout=cashout, start_time=start_time, is_live=is_live,
                                    wait_for_event=wait_for_event, **kwargs)

    def add_autotest_esports_event(self, start_time=None, markets=None, cashout=True,
                                                   is_live=False, is_upcoming=False, wait_for_event=True, **kwargs):
        return self.add_sport_event(class_id=self.esports_config.esport_autotest.class_id,
                                    category_id=self.esports_config.category_id,
                                    type_id=self.esports_config.esport_autotest.autotest_league.type_id,
                                    markets=markets,
                                    default_market_name=self.esports_config.esport_autotest.autotest_league.market_name,
                                    market_template_id=self.esports_config.esport_autotest.autotest_league.market_template_id,
                                    start_time=start_time, cashout=cashout, is_live=is_live, is_upcoming=is_upcoming,
                                    wait_for_event=wait_for_event, **kwargs)

    def update_event_start_time(self, eventID, start_time):
        params = '?action=hierarchy::event::H_update&id={0}&start_time={1}&flags=AVA,BL,FI'.format(eventID, start_time)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def change_selection_name(self, selection_id, new_selection_name):
        url = '{backoffice}/hierarchy/selection/{id}' \
            .format(backoffice=self.site, id=selection_id)
        params = '?action=hierarchy::selection::H_update&id={id}&desc={name}&exact_flags=Y' \
            .format(id=selection_id, name=quote(new_selection_name, safe=''))
        url = url + params
        do_request(url=url, cookies=self.site_cookies)

    def change_event_state(self, event_id, displayed=False, active=False):
        """
        Changing event state. By default - makes event Suspended and Not Displayed
        :param event_id: event id
        :param displayed: True or False
        :param active: True or False (suspended)
        """
        displayed = 'Y' if displayed else 'N'
        active = 'A' if active else 'S'
        url = '{0}/hierarchy/event/{1}'.format(self.site, event_id)
        params = '?action=hierarchy::event::H_update' \
                 '&id={event_id}' \
                 '&displayed={displayed}' \
                 '&status={status}' \
                 '&exact_flags=Y' \
            .format(event_id=event_id, displayed=displayed, status=active)
        url = url + params
        do_request(url=url, cookies=self.site_cookies)

    def link_selection_to_event(self, selection_id, eventID, linked=True):
        """
        :param selection_id: int
        :type selection_id: int
        :type eventID: int
        :param linked: if linked True than take eventID else '' unlinked
        :return:
        """
        linked = eventID if linked else ''
        params = {
            'action': 'hierarchy::selection::H_update',
            'id': selection_id,
            'evoc_ev_linked_ids': linked + ' ',
            'exact_flags': 'Y'
        }
        do_request(url=self.site, cookies=self.site_cookies, params=params)

    def change_selection_state(self, selection_id, displayed=False, active=False, wait_time=3, **kwargs):
        """
        Changing selection state. By default - makes selection Suspended and Not Displayed
        :param selection_id: event id
        :param displayed: True or False
        :param active: True or False (suspended)
        :param wait_time: How many seconds should application wait before next actions. Used in 'sleep'.
        """
        displayed = 'Y' if displayed else 'N'
        active = 'A' if active else 'S'
        value = 'Y' if kwargs.get('fixed_stake_limits') else 'N'
        url = '{0}/hierarchy/selection/{1}'.format(self.site, selection_id)
        params = '?action=hierarchy::selection::H_update' \
                 '&id={selection_id}' \
                 '&status={active}' \
                 '&fixed_stake_limits={value}' \
                 '&displayed={displayed}' \
                 '&exact_flags=Y' \
            .format(selection_id=selection_id, active=active, displayed=displayed, value=value)
        url = url + params
        do_request(url=url, cookies=self.site_cookies)
        sleep(wait_time)

    def change_market_bir_delay(self, event_id, market_id, bir_delay=10):
        """
        Changing 'bir delay' parameter for market. Default value = 10
        """
        url = self.site
        params = '?action=hierarchy::market::H_update' \
                 '&id={market_id}' \
                 '&bir_delay={bir_delay}' \
                 '&exact_flags=Y' \
                 '&ev_id={event_id}'.format(market_id=market_id, event_id=event_id, bir_delay=bir_delay)
        url += params
        do_request(url=url, cookies=self.site_cookies)

    def change_market_state(self, event_id, market_id, displayed=False, active=False):
        """
        Changing market state. By default - makes market Suspended and Not Displayed
        """
        active = 'A' if active else 'S'
        displayed = 'Y' if displayed else 'N'
        url = '{0}/hierarchy/event/{1}'.format(self.site, event_id)
        params = '?action=hierarchy::event::H_update&id={event_id}' \
                 '&market_status_{market_id}={active}' \
                 '&market_displayed_{market_id}={displayed}' \
                 '&sub_id={market_id}' \
                 '&sub_level=market' \
                 '&exact_flags=Y'.format(event_id=event_id, market_id=market_id, displayed=displayed, active=active)
        url += params
        do_request(url=url, cookies=self.site_cookies)

    def make_market_special(self, event_id, market_id, market_template_id, sort_market='MR', status='Y', flags='SM,SP'):
        """
        Make market special/ not special
        :param event_id: event id
        :param market_id: market id
        :param market_template_id: market template id
        :param sort_market: sort market
        :param status: Y or N
        :param flags: SM,SP or empty str
        """
        params = (('action', 'hierarchy::market::H_update'),
                  ('id', market_id),
                  ('flag_SM', 'Y'),
                  ('flag_SP', status),
                  ('flags', flags),
                  ('ev_id', event_id),
                  ('ev_oc_grp_id', market_template_id),
                  ('sort', sort_market),)
        do_request(url=self.site, cookies=self.site_cookies, params=params)

    def change_racing_market_lp_price_status(self, event_id, market_id, market_template_id, status=True):
        url = '{site}/ti'.format(site=self.site)
        lp_status = 'Y' if status else 'N'
        params = '?action=hierarchy::market::H_update' \
                 '&id={market_id}' \
                 '&lp_avail={lp_status}' \
                 '&flags=' \
                 '&ev_id={event_id}' \
                 '&ev_oc_grp_id={market_template_id}' \
                 '&sort=--' \
                 '&class_sort=HR' \
                 '&ew_with_bet=N' \
                 '&ew_avail=N'.format(market_id=market_id, lp_status=lp_status, event_id=event_id,
                                      market_template_id=market_template_id)
        url += params
        do_request(url=url, cookies=self.site_cookies)

    def change_racing_market_forecast_tricast_status(self, event_id, market_id, market_template_id, category_id, forecast_status=True,
                                                     tricast_status=True):
        url = '{site}/ti'.format(site=self.site)
        class_sort = 'HR' if category_id == self.horseracing_config.category_id else 'GH'
        forecast = 'Y' if forecast_status else 'N'
        tricast = 'Y' if tricast_status else 'N'
        params = (
            ('action', 'hierarchy::market::H_update'),
            ('id', market_id),
            ('fc_avail', forecast),
            ('tc_avail', tricast),
            ('exact_flags', 'Y'),
            ('ev_id', event_id),
            ('ev_oc_grp_id', market_template_id),
            ('sort', '--'),
            ('class_sort', class_sort),
        )
        do_request(url=self.site, params=params, cookies=self.site_cookies)

    def change_price(self, selection_id, price):
        params = '?action=hierarchy::selection::H_update' \
                 '&id={selection_id}' \
                 '&lp_price={price}' \
                 '&exact_flags=Y'.format(selection_id=selection_id, price=quote(price))
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def change_score(self, event_id: str, team1_name: str, team2_name: str, home_score: str, away_score: str,
                     serving='home_team', home_set_scores='1', away_set_scores='1', home_game_score='2',
                     away_game_score='2', points_score=False, game_points_score=False, cricket_score=False) -> None:
        """
        :param event_id: event id
        :param team1_name: the first team name
        :param team2_name: the second team name
        :param home_score: score for home player
        :param away_score: score for away score player
        :param serving: '*' near player name is responsible for serving
        :param home_set_scores: Set score for home player
        :param away_set_scores: Set score for away player
        :param home_game_score: Game score for home player
        :param away_game_score: Game score for away player
        :param points_score: True if score template with points
        :param game_points_score: True if score template with Game score and points score
        :param cricket_score: True for Cricket event
        """
        if points_score:
            if serving == 'away_team':
                name = f'|{team1_name}| ({home_set_scores}) {home_score}-{away_score} ({away_set_scores}) |{team2_name}*|'
            else:
                name = f'|{team1_name}*| ({home_set_scores}) {home_score}-{away_score} ({away_set_scores}) |{team2_name}|'
        elif game_points_score:
            if serving == 'away_team':
                name = f'|{team1_name}| ({home_set_scores}) {home_game_score} {home_score}-{away_score} {away_game_score} ({away_set_scores}) |{team2_name}*|'
            else:
                name = f'|{team1_name}*| ({home_set_scores}) {home_game_score} {home_score}-{away_score} {away_game_score} ({away_set_scores}) |{team2_name}|'
        elif cricket_score:
            name = f'|{team1_name}| {home_score} v |{team2_name}| {away_score}'
        else:
            name = f'|{team1_name}| {home_score}-{away_score} |{team2_name}|'

        params = (
            ('action', 'hierarchy::event::H_update'),
            ('id', event_id),
            ('name', name),
            ('exact_flags', 'Y')
        )
        url = self.site
        do_request(url=url, params=params, cookies=self.site_cookies)

    def delete_event(self, eventID):  # do not use it
        params = '?action=hierarchy::event::H_delete' \
                 '&id=%s' % eventID
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def change_event_cashout_status(self, event_id, cashout_available):
        cashout_avail = 'Y' if cashout_available else 'N'
        params = '?action=hierarchy::event::H_update' \
                 '&id={event_id}' \
                 '&cashout_avail={cashout_avail}' \
                 '&exact_flags=Y'.format(event_id=event_id, cashout_avail=cashout_avail)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def change_event_enhanced_odds_status(self, event_id, enhanced_odds_available):
        enhanced_odds_avail = 'Y' if enhanced_odds_available else 'N'
        params = '?action=hierarchy::event::H_update' \
                 '&id={event_id}' \
                 '&enhanced_odds_avail={enhanced_odds_avail}' \
                 '&exact_flags=Y'.format(event_id=event_id, enhanced_odds_avail=enhanced_odds_avail)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def update_event_disporder(self, eventID, disporder_value):
        """
        Update Event Disporder
            :param eventID: event id
            :param disporder_value: new disporder value
        """
        params = '?action=hierarchy::event::H_update&id={0}&disporder={1}&exact_flags=Y'.format(eventID, disporder_value)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def result_selection(self, selection_id, market_id, event_id, result='W', place=2, **kwargs):
        """
        :param result: one of W (Win), L (Lose), V (Void), P (Place)
        :param place: default 2, if result Win then 1
        """
        place_ = 1 if result == 'W' else place
        price = kwargs.get('price', None)
        if price is None:
            price = '{0}/{1}'.format(randint(1, 10), randint(10, 20)) if result in ['W', 'P', 'L'] else ''
        params = '?action=hierarchy::result::H_result' \
                 '&id={0}' \
                 '&selection_{1}_{0}=Y' \
                 '&result_{1}_{0}={3}' \
                 '&place_{1}_{0}={4}' \
                 '&sp_{1}_{0}={5}' \
                 '&exact_flags=Y' \
                 '&level=selection' \
                 '&ev_id={2}' \
                 '&ev_mkt_ids={1}'.format(selection_id, market_id, event_id, result, place_, quote(price))

        if result == '-':
            params = '?action=hierarchy::result::H_result' \
                     '&id={0}' \
                     '&selection_{1}_{0}=Y' \
                     '&result_{1}_{0}={3}' \
                     '&exact_flags=Y' \
                     '&level=selection' \
                     '&ev_id={2}' \
                     '&ev_mkt_ids={1}'.format(selection_id, market_id, event_id, result, place_, quote(price))

        url = self.site + params
        resp_dict = do_request(url=url, cookies=self.site_cookies)

        if kwargs.get('wait_for_update'):
            try:
                if resp_dict['notifications'][0]['type'] == 'error':
                    raise OBException(resp_dict['notifications'][0]['msg'])
            except KeyError:
                self._logger.warning('There\'s no "type" in the response')
            wait_for_result(lambda: 'Processing' not in self.get_selection_result(action='result',
                                                                                  selection_id=selection_id),
                            poll_interval=2,
                            name='Wait for selection: %s is resulted by absence of status "Processing"' % selection_id)
            return price

    def get_selection_result(self, action, selection_id):
        url = self.site + \
              '/hierarchy/selection/{0}/result'.format(selection_id)
        r = do_request(url=url, method='GET', cookies=self.site_cookies, load_response=False)
        page = html.fromstring(r)
        xpath = '//*[contains(@id, "result_{0}") and contains(@id, "{1}")]'.format(action, selection_id)
        result = page.xpath(xpath)
        try:
            text = result[0].text
            text = ''.join(t for t in text if not t.isspace())
            self._logger.info('*** Found text "%s"' % text)
            return text
        except IndexError as e:
            raise OBException('No result found for selection id %s or error occurred %s' % (selection_id, e))

    def handicap_result_selection(self, selection_ids, market_id, event_id, result='L'):
        if result == 'L':
            result = 0
            params = '?action=hierarchy::result::H_result' \
                     '&id={selection_id}' \
                     '&ft_score_h_{market_id}={result}' \
                     '&ft_score_a_{market_id}={result}' \
                     '&exact_flags=Y' \
                     '&level=selection' \
                     '&ev_id={event_id}' \
                     '&ev_mkt_ids={market_id}'.format(selection_id=selection_ids['tie'],
                                                      market_id=market_id,
                                                      event_id=event_id,
                                                      result=result)
            url = self.site + params
            resp_dict = do_request(url=url, cookies=self.site_cookies)
            try:
                if resp_dict['notifications'][0]['type'] == 'error':
                    raise OBException(resp_dict['notifications'][0]['msg'])
                else:
                    pass
            except KeyError:
                self._logger.warning('There\'s no "type" in the response')
            wait_for_result(lambda: 'Yes' in self.get_selection_result(
                action='confirmed', selection_id=selection_ids['tie']),
                            poll_interval=2,
                            name='Wait for selection: %s result is confirmed by status "Yes"' % selection_ids['tie'])

        if result == 'V':
            params = '?action=hierarchy::result::H_result' \
                     '&id={market_id}' \
                     '&link_{market_id}_bulk=Y' \
                     '&selection_{market_id}_{team1}=Y' \
                     '&selection_{market_id}_{tie}=Y' \
                     '&selection_{market_id}_{team2}=Y' \
                     '&result_{market_id}_{tie}={result}' \
                     '&result_{market_id}_{team1}=H' \
                     '&result_{market_id}_{team2}=H' \
                     '&exact_flags=Y' \
                     '&level=market' \
                     '&ev_id={event_id}' \
                     '&ev_mkt_ids={market_id}'.format(tie=selection_ids['tie'],
                                                      team1=selection_ids['won'],
                                                      team2=selection_ids['lost'],
                                                      market_id=market_id,
                                                      event_id=event_id,
                                                      result=result)
            self._perform_handicap_request(params, selection_ids)
            self._prepare_confirm_handicap_void(selection_ids, market_id, event_id)
            self._perform_handicap_request(params, selection_ids)

        if result == 'W':
            result = 5
            params = '?action=hierarchy::result::H_result' \
                     '&id={selection_id}' \
                     '&ft_score_h_{market_id}={result}' \
                     '&ft_score_a_{market_id}=0' \
                     '&exact_flags=Y' \
                     '&level=selection' \
                     '&ev_id={event_id}' \
                     '&ev_mkt_ids={market_id}'.format(selection_id=selection_ids['won'],
                                                      market_id=market_id,
                                                      event_id=event_id,
                                                      result=result)

            url = self.site + params
            resp_dict = do_request(url=url, cookies=self.site_cookies)
            try:
                if resp_dict['notifications'][0]['type'] == 'error':
                    raise OBException(resp_dict['notifications'][0]['msg'])
                else:
                    pass
            except KeyError:
                self._logger.warning('There\'s no "type" in the response')
            self._prepare_confirm_handicap_won(selection_ids, market_id, event_id)
            self._perform_handicap_request(params, selection_ids)

    def _perform_handicap_request(self, params, selection_ids):
        url = self.site + params
        resp_dict = do_request(url=url, cookies=self.site_cookies)
        try:
            if resp_dict['notifications'][0]['type'] == 'error':
                raise OBException(resp_dict['notifications'][0]['msg'])
            else:
                pass
        except KeyError:
            self._logger.warning('There\'s no "type" in the response')
        for selection_id in selection_ids.values():
            wait_for_result(lambda: 'Yes' in self.get_selection_result(action='confirmed', selection_id=selection_id),
                            poll_interval=2,
                            name='Wait for selection: %s result is confirmed by status "Yes"' % selection_id)

    # is not used yet
    def _prepare_confirm_handicap_lost(self, selection_ids, market_id, event_id):
        params = '?action=hierarchy::result::H_confirm' \
                 '&id={market_id}' \
                 '&link_{market_id}_bulk=Y' \
                 '&result_{market_id}_{team1}=H' \
                 '&result_{market_id}_{tie}=H' \
                 '&result_{market_id}_{team2}=H' \
                 '&exact_flags=Y' \
                 '&level=selection' \
                 '&ev_id={event_id}' \
                 '&market_{market_id}=Y' \
                 '&ev_mkt_ids={market_id}'.format(tie=selection_ids['tie'],
                                                  team1=selection_ids['won'],
                                                  team2=selection_ids['lost'],
                                                  market_id=market_id,
                                                  event_id=event_id)
        return params

    def _prepare_confirm_handicap_void(self, selection_ids, market_id, event_id):
        params = '?action=hierarchy::result::H_confirm' \
                 '&id={market_id}' \
                 '&link_{market_id}_bulk=Y' \
                 '&result_{market_id}_{team1}=H' \
                 '&result_{market_id}_{tie}=V' \
                 '&result_{market_id}_{team2}=H' \
                 '&exact_flags=Y' \
                 '&level=market' \
                 '&ev_id={event_id}' \
                 '&market_{market_id}=Y' \
                 '&ev_mkt_ids={market_id}'.format(tie=selection_ids['tie'],
                                                  team1=selection_ids['won'],
                                                  team2=selection_ids['lost'],
                                                  market_id=market_id,
                                                  event_id=event_id)
        return params

    def _prepare_confirm_handicap_won(self, selection_ids, market_id, event_id):
        params = '?action=hierarchy::result::H_confirm' \
                 '&id={market_id}' \
                 '&link_{market_id}_bulk=Y' \
                 '&result_{market_id}_{team2}=H' \
                 '&result_{market_id}_{team1}=H' \
                 '&result_{market_id}_{tie}=H' \
                 '&exact_flags=Y' \
                 '&level=market' \
                 '&ev_id={event_id}' \
                 '&market_{market_id}=Y' \
                 '&ev_mkt_ids={market_id}'.format(tie=selection_ids['tie'],
                                                  team1=selection_ids['won'],
                                                  team2=selection_ids['lost'],
                                                  market_id=market_id,
                                                  event_id=event_id)
        return params

    def settle_handicap_result(self, selection_id, event_id):
        params = '?action=hierarchy::result::H_settle' \
                 '&id={selection_id}' \
                 '&link_{selection_id}_bulk=Y' \
                 '&exact_flags=Y' \
                 '&level=market' \
                 '&ev_id={event_id}' \
                 '&market_{selection_id}=Y' \
                 '&ev_mkt_ids={selection_id}'.format(selection_id=selection_id,
                                                     event_id=event_id)
        return params

    def confirm_result(self, selection_id, market_id, event_id, result='W', is_confirm=True, **kwargs):
        wait_for_state = 'Yes'
        params = '?action=hierarchy::result::H_confirm' \
                 '&id={selection_id}' \
                 '&selection_{market_id}_{selection_id}=Y' \
                 '&result_{market_id}_{selection_id}={result}' \
                 '&exact_flags=Y' \
                 '&level=selection' \
                 '&ev_id={event_id}' \
                 '&ev_mkt_ids={market_id}'.format(selection_id=selection_id, market_id=market_id,
                                                  result=result, event_id=event_id)
        if not is_confirm:
            params = params.replace('H_confirm', 'H_unconfirm')
            params = params.replace('&result_{market_id}_{selection_id}={result}'.format(
                selection_id=selection_id, market_id=market_id, result=result), '')
            wait_for_state = 'No'
        url = self.site + params
        resp_dict = do_request(url=url, cookies=self.site_cookies)
        if kwargs.get('wait_for_update'):
            try:
                if resp_dict['notifications'][0]['type'] == 'error':
                    raise OBException(resp_dict['notifications'][0]['msg'])
                else:
                    pass
            except KeyError:
                self._logger.warning('There\'s no "type" in the response')
            wait_for_result(lambda: wait_for_state in self.get_selection_result(
                action='confirmed', selection_id=selection_id),
                            poll_interval=2,
                            name='Wait for selection: %s result is confirmed state is: %s by status "%s"'
                                 % (selection_id, is_confirm, wait_for_state))

    def change_is_off_flag(self, event_id, is_off, gvm=False):
        is_off_status = 'Y' if is_off else 'N'
        gvm_status = 'Y' if gvm else 'N'
        if gvm:
            params = (('action', 'hierarchy::event::H_update'),
                      ('id', event_id),
                      ('is_off', is_off_status),
                      ('flag_GVM', gvm_status),
                      ('flags', 'GVM,'),
                      ('exact_flags', 'Y'))
        else:
            params = (('action', 'hierarchy::event::H_update'),
                      ('id', event_id),
                      ('is_off', is_off_status),
                      ('exact_flags', 'Y'))
        do_request(url=self.site, cookies=self.site_cookies, params=params)

    def settle_result(self, selection_id, market_id, event_id, result='W', is_settle=True, **kwargs):
        wait_for_state = 'Yes'
        params = '?action=hierarchy::result::H_settle' \
                 '&id={selection_id}' \
                 '&selection_{market_id}_{selection_id}=Y' \
                 '&result_{market_id}_{selection_id}={result}' \
                 '&exact_flags=Y' \
                 '&level=selection' \
                 '&ev_id={event_id}' \
                 '&ev_mkt_ids={market_id}'.format(selection_id=selection_id, market_id=market_id,
                                                  result=result, event_id=event_id)
        if not is_settle:
            params = params.replace('H_settle', 'H_unsettle')
            params = params.replace('&result_{market_id}_{selection_id}={result}'.format(
                selection_id=selection_id, market_id=market_id, result=result), '')
            wait_for_state = 'No'
        url = self.site + params
        resp_dict = do_request(url=url, cookies=self.site_cookies)
        if kwargs.get('wait_for_update'):
            try:
                if resp_dict['notifications'][0]['type'] == 'error':
                    raise OBException(resp_dict['notifications'][0]['msg'])
                else:
                    pass
            except KeyError:
                self._logger.warning('There\'s no "type" in the response')
            wait_for_result(lambda: wait_for_state
                            in self.get_selection_result(action='settled', selection_id=selection_id),
                            poll_interval=2,
                            name='Wait for selection: "%s" result is settled state is: %s'
                                 % (selection_id, is_settle))

    def change_handicap_market_value(self, event_id, market_id, market_template_id, new_handicap_value):
        params = '?action=hierarchy::market::H_update' \
                 '&id={market_id}' \
                 '&hcap_value={new_handicap_value}' \
                 '&flags=' \
                 '&ev_id={event_id}' \
                 '&ev_oc_grp_id={market_template_id}' \
                 '&sort=MH'.format(market_id=market_id, event_id=event_id, new_handicap_value=new_handicap_value,
                                   market_template_id=market_template_id)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def make_event_live(self, market_id, event_id, is_live=True):
        """
        :param event_id: eventID of existing non-live event
        :param market_id: marketID for Match Result market
        """
        is_off = 'Y' if is_live else 'N'
        bet_in_run = 'Y' if is_live else 'N'

        params = '?action=hierarchy::event::H_update' \
                 '&id={event_id}' \
                 '&flag_BL=Y' \
                 '&is_off={is_off}' \
                 '&flags=AVA,BL,FI,'.format(event_id=event_id, is_off=is_off)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

        params = '?action=hierarchy::market::H_update' \
                 '&id={market_id}' \
                 '&bet_in_run={bet_in_run}' \
                 '&exact_flags=Y' \
                 '&ev_id={event_id}' \
                 '&sort=MR'.format(market_id=market_id, event_id=event_id, bet_in_run=bet_in_run)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)
        sleep(5)
        # sleep needed as event is not shown immediately as live and not present on In-Play tab/page

    def change_min_max_bet_limits(self, id, level='event', min_bet='', max_bet='', max_mult_bet=''):
        params = '?action=hierarchy::' \
                 '{level}' \
                 '::H_update' \
                 '&id={id}' \
                 '&min_bet={min_bet}' \
                 '&max_bet={max_bet}' \
                 '&max_mult_bet={max_mult_bet}' \
                 '&exact_flags=Y'.format(level=level, id=id, min_bet=min_bet, max_bet=max_bet,
                                         max_mult_bet=max_mult_bet)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)

    def add_private_market(self, trigger_market, offered_market):
        """
        TODO: currently doesn't work.
        :param trigger_market: MarketID bet on which will trigger offer (Preferably "Match Betting" Marker)
        :param offered_market: MarketID of Private Market which will be offered
        :return:
        """
        site = self.site[:-2]
        history_list_trigger = '&HistoryList=%3faction%3dFREEBETS%3a%3aDoOfferSearch%26name%3d%26retro%3d%26' \
                               'retro_status%3d%26start_date_from%3d%26start_date_to%3d%26end_date_from%3d%26' \
                               'end_date_to%3d%26channel%3d%26lang%3d%26well_formed%3d%26effective%3dY%26' \
                               'category_search_type%3dignore%26trigger_type_search_type%3dignore%26' \
                               'token_type_search_type%3dignore%26offer_cat_ids%3d%26trigger_type_codes%3d%26' \
                               'token_type_codes%3d%26adhoc_offer%3d+%3faction%3dFREEBETS%3a%3aGoOffer%26OfferID%3d2208'

        history_list_offer = '&HistoryList=%3faction%3dFREEBETS%3a%3aDoOfferSearch%26name%3d%26retro%3d%26' \
                             'retro_status%3d%26start_date_from%3d%26start_date_to%3d%26end_date_from%3d%26' \
                             'end_date_to%3d%26channel%3d%26lang%3d%26well_formed%3d%26effective%3dY%26' \
                             'category_search_type%3dignore%26trigger_type_search_type%3dignore%26' \
                             'token_type_search_type%3dignore%26offer_cat_ids%3d%26trigger_type_codes%3d%26' \
                             'token_type_codes%3d%26adhoc_offer%3d+%3faction%3dFREEBETS%3a%3aGoOffer%26OfferID%3d2208'

        url_trigger = site + 'camp_mgr' \
                             '?action=FREEBETS::DoTriggerLevel' \
                             '&TriggerID=22972' \
                             '&Level=MARKET' \
                             '&ID={MarketID}' \
                             '&Submit=Insert'.format(MarketID=trigger_market) + history_list_trigger
        do_request(url=url_trigger, method='GET', load_response=False, cookies=self.site_cookies)
        url_offer = site + 'camp_mgr' \
                           '?action=FREEBETS::DoRestrictedSetLink' \
                           '&TokenID=2047' \
                           '&Level=MARKET' \
                           '&ID={MarketID}' \
                           '&OfferID=2208' \
                           '&Submit=Insert' \
                           '&TokenType=ACCESS'.format(MarketID=offered_market) + history_list_offer
        do_request(url=url_offer, method='GET', load_response=False, cookies=self.site_cookies)

    def grant_freebet(self, username, freebet_value=1, level=None, id=None, expiration_date=None):
        redemption = self.backend.ob.freebets.get(level, self.backend.ob.freebets.any) \
            if level else self.backend.ob.freebets.any
        redemption_name, redemption_value = redemption.name, redemption.redemption_value

        fb = Freebet(env=self.env, brand=self.brand, redemption_value=redemption_value, freebet_name=redemption_name)
        fb.get_custid(username=username)
        fb.give_offer(freebet_value=freebet_value, expiration_date=expiration_date)
        if id:
            self._logger.info('*** Adding offer for level: "%s", id: "%s"' % (level, id))
            fb.add_freebet_to_level(level=level, id=id)
        self._logger.info('*** Freebet offer is granted for username "%s"' % username)

    def grant_freeride(self, offer_id, username, freeride_value=1, expiration_date=None):
        redemption = self.backend.ob.freeride.any
        redemption_name, redemption_value = redemption.name, redemption.redemption_value

        fr = Freeride(env=self.env, brand=self.brand, redemption_value=redemption_value, freeride_name=redemption_name)
        fr.get_custid(username=username)
        if offer_id is None:
            offer_id = self.backend.ob.freeride.general_offer.offer_id

        fr.give_offer(token_value=freeride_value, expiration_date=expiration_date, offer_id=offer_id, days=1)
        self._logger.info('*** Freeride offer is granted for username "%s"' % username)

    def get_user_id(self, username, level=None, raise_exceptions=True):
        redemption = self.backend.ob.freebets.get(level, self.backend.ob.freebets.any) \
            if level else self.backend.ob.freebets.any
        redemption_name, redemption_value = redemption.name, redemption.redemption_value

        fb = Freebet(env=self.env, brand=self.brand, redemption_value=redemption_value, freebet_name=redemption_name)
        user_id = fb.get_custid(username=username, raise_exceptions=raise_exceptions)
        return user_id

    def grant_odds_boost_token(self, username, token_value=1, level=None, id=None, expiration_date=None, offer_id=None):
        redemption = self.backend.ob.odds_boost_offer.get(level, self.backend.ob.odds_boost_offer.any) \
            if level else self.backend.ob.odds_boost_offer.any
        redemption_name, redemption_value = redemption.name, redemption.redemption_value

        ob = OddsBoost(env=self.env, brand=self.brand, redemption_value=redemption_value,
                       odds_boost_token_name=redemption_name)
        ob.get_custid(username=username)
        if offer_id is None:
            offer_id = self.backend.ob.odds_boost_offer.general_offer.offer_id

        ob.give_offer(token_value=token_value, expiration_date=expiration_date, offer_id=offer_id)
        if id:
            self._logger.info('*** Adding Odds Boost token for level: "%s", id: "%s"' % (level, id))
            ob.add_odds_boost_token_to_level(level=level, id=id)
        self._logger.info('*** Odds Boost token is granted for username "%s"' % username)

    def change_double_your_winnings_promotion_market_state(self, market_id, market_template_id, event_id,
                                                           available=True):
        flag_DYW = 'Y' if available else 'N'
        flags = 'DYW,SM,SP' if available else 'SM,SP'
        url = self.site + '?action=hierarchy::market::H_update' \
                          '&id={market_id}' \
                          '&flag_DYW={flag_DYW}' \
                          '&flags={flags}' \
                          '&ev_id={event_id}' \
                          '&ev_oc_grp_id={market_template_id}' \
                          '&sort=MR'.format(market_id=market_id, market_template_id=market_template_id,
                                            event_id=event_id, flag_DYW=flag_DYW, flags=flags)
        do_request(url=url, cookies=self.site_cookies)

    def change_racing_promotion_state(self, promotion_name, market_id: str, event_id: str, available: bool = True,
                                      level: str = 'market'):
        """
        :param promotion_name: hardcoded name of promotion (fallers_insurance, beaten_by_a_length, extra_place_race,
        featured_racing_types)
        :param market_id: market ID
        :param event_id: event ID
        :param available: set desired promotion as True or False
        :param level: level on which perform change. Event or market level
        """
        promotions = {'fallers_insurance': 'FI' if level == 'market' else 'FIN',
                      'beaten_by_a_length': 'BBAL' if level == 'market' else 'BBL',
                      'extra_place_race': 'EPR',
                      # There is no 'Featured Racing Types' promotion on market level
                      'featured_racing_types': 'FRT' if level == 'event' else ''}
        if promotion_name not in promotions:
            raise OBException('*** Not present')
        promotion_abbreviation_name = promotions[promotion_name]
        flag_availability = 'Y' if available else 'N'
        flags = promotion_abbreviation_name if available else ''
        if level == 'market':
            if type(market_id) not in (str, int):
                raise OBException(
                    f'Wrong data type of market_id provided. Expecting string, received {type(market_id)}.')
            event_or_market_id = market_id
        else:
            if type(event_id) not in (str, int):
                raise OBException(
                    f'Wrong data type of event_id provided. Expecting string, received {type(event_id)}.')
            event_or_market_id = event_id

        url = self.site + '?action=hierarchy::{level}::H_update' \
                          '&id={event_or_market_id}' \
                          '&flag_{promotion_abbreviation_name}={flag_availability}' \
                          '&flags={flags}' \
                          '&ev_id={event_id}'.format(level=level, event_or_market_id=event_or_market_id, flags=flags,
                                                     promotion_abbreviation_name=promotion_abbreviation_name,
                                                     flag_availability=flag_availability, event_id=event_id,)
        do_request(url=url, cookies=self.site_cookies)

    def update_selection_result(self, event_id, market_id, selection_id, result='W', settle=True, **kwargs):
        self.result_selection(selection_id=selection_id, market_id=market_id,
                              event_id=event_id, result=result, **kwargs)
        self.confirm_result(selection_id=selection_id, market_id=market_id,
                            event_id=event_id, result=result)
        self.settle_result(selection_id=selection_id, market_id=market_id, event_id=event_id,
                           result=result, is_settle=settle)

    def add_dividend_for_existing_event(self, category_id, event_id, market_id, forecast=True, tricast=True, **kwargs):
        forecast_dividend = kwargs.get('forecast_dividend', '2.44')
        tricast_dividend = kwargs.get('tricast_dividend', '1.33')
        class_sort = 'HR' if category_id == self.horseracing_config.category_id else 'GH'

        from crlat_siteserve_client.siteserve_client import SiteServeRequests
        s = SiteServeRequests(env=self.env, class_id=self.backend.ti.horse_racing.horse_racing_live.class_id,
                              category_id=self.horseracing_config.category_id, brand=self.brand)
        event = s.ss_event_to_outcome_for_event(event_id=event_id)

        for market in event[0]['event']['children']:
            if market['market']['id'] == market_id:
                market_template_id = event[0]['event']['children'][0]['market']['templateMarketId']
                break

        selections_ids = []
        for selection in event[0]['event']['children'][0]['market']['children']:
            selections_ids.append(selection['outcome']['id'])

        if tricast:
            selection_id_1, selection_id_2, selection_id_3 = selections_ids[:3]
            tricast_params = (
                ('dividend_ins_seln_0_1', selection_id_1),
                ('dividend_ins_seln_1_1', selection_id_2),
                ('dividend_ins_seln_2_1', selection_id_3),
                ('dividend_ins_dividend_1', tricast_dividend),
            )
        if forecast:
            selection_id_1, selection_id_2 = selections_ids[:2]
            forecast_params = (
                ('dividend_ins_seln_0_0', selection_id_1),
                ('dividend_ins_seln_1_0', selection_id_2),
                ('dividend_ins_dividend_0', forecast_dividend),
            )
        base_params = (
            ('action', 'hierarchy::market::H_update'),
            ('id', market_id),
            ('exact_flags', 'Y'),
            ('ev_id', event_id),
            ('ev_oc_grp_id', market_template_id),
            ('sort', '--'),
            ('class_sort', class_sort),
            ('ew_with_bet', 'N'),
            ('ew_avail', 'Y'),
            ('dividend_ins_type_0', 'FC'),
            ('dividend_ins_action_0', 'Insert'),
            ('dividend_ins_type_1', 'TC'),
            ('dividend_ins_action_1', 'Insert')
        )
        params = base_params + forecast_params if forecast else base_params
        params = params + tricast_params if tricast else params

        do_request(url=self.site, params=params, cookies=self.site_cookies)

    def _add_dividend_to_market(self, category_id, type_id, event_id, default_market_template_id,
                                default_market_name, selection_ids, **kwargs):

        class_sort = 'HR' if category_id == self.horseracing_config.category_id else 'GH'
        forecast_dividend = kwargs.get('forecast_dividend', '2.44')
        tricast_dividend = kwargs.get('tricast_dividend', '1.33')

        for market_short_name, market_id in self.market_ids.items():
            if market_short_name.isdigit():
                market_template_id = default_market_template_id
                market_short_name = default_market_name.replace('|', '').replace(' ', '_').lower()
            else:
                _, market_template_id = self._get_racing_market_template_name_and_id(type_id=type_id,
                                                                                     market_short_name=market_short_name)
            market_selections = selection_ids.get(market_short_name) if selection_ids.get(market_short_name) else selection_ids
            selection_ids_ = list(market_selections.values())
            if len(selection_ids_) < 3:
                raise OBException('You should have at least 3 market selections to be able to add dividend')
            selection_id_1, selection_id_2, selection_id_3 = selection_ids_[:3]

            params = (
                ('action', 'hierarchy::market::H_update'),
                ('id', market_id),
                ('dividend_ins_seln_0_0', selection_id_1),
                ('dividend_ins_seln_1_0', selection_id_2),
                ('dividend_ins_dividend_0', forecast_dividend),
                ('dividend_ins_seln_0_1', selection_id_1),
                ('dividend_ins_seln_1_1', selection_id_2),
                ('dividend_ins_seln_2_1', selection_id_3),
                ('dividend_ins_dividend_1', tricast_dividend),
                ('exact_flags', 'Y'),
                ('ev_id', event_id),
                ('ev_oc_grp_id', market_template_id),
                ('sort', '--'),
                ('class_sort', class_sort),
                ('ew_with_bet', 'N'),
                ('ew_avail', 'Y'),
                ('dividend_ins_type_0', 'FC'),
                ('dividend_ins_action_0', 'Insert'),
                ('dividend_ins_type_1', 'TC'),
                ('dividend_ins_action_1', 'Insert')
            )

            do_request(url=self.site, params=params, cookies=self.site_cookies)

    def get_tolerance_value(self):
        url = self.admin
        params = '?action=ADMIN::OPENBET_CFG::GoOpenbetCfgList&CfgGrpName=Cashout%20Tolerance'
        html_text = do_request(url=url + params, cookies=self.site_cookies, method='GET', load_response=False)
        etree_element = html.fromstring(html_text)
        selector = '//tr[.//*[contains(text(), "CASHOUT_TOLERANCE_PERCENTAGE")]]//input'
        element = etree_element.xpath(selector)
        if not element:
            raise OBException('cannot get CASHOUT_TOLERANCE_PERCENTAGE')
        tolerance_value = element[0].value
        return tolerance_value

    # Lotto
    def get_lotto_bet_id(self, sub_id: str) -> str:
        """
        Gets Lotto bet id by sub id parameter which can be taken from bet receipt.
        :param sub_id: specifies bet sub id
        :return: bet id
        """
        url = self.admin
        params = (
            ('action', 'ADMIN::BET::GoXGameSub'),
            ('SubId', sub_id),
        )
        html_text = do_request(url=url, params=params, cookies=self.site_cookies, method='GET', load_response=False)
        etree_element = html.fromstring(html_text)
        selector = '//a[contains(@href, "GoXGameReceipt&BetId=")]'
        element = etree_element.xpath(selector)
        if not element:
            raise OBException('Cannot get Lotto Bet Id')
        bet_id = element[0].text
        return bet_id

    def settle_lotto_bet(self, bet_id='', bet_sub_id='', winnings='', refund='', submit_name='StlBet'):
        """
        Settles lotto bet. As a result, depending on selected parameters, bet can be won, canceled or lost.
        :param bet_id: specifies bet id. If not set can be extracted using bet_sub_id
        :param bet_sub_id: specifies bet sub id. Is used for extracting bet_id only
                           so if bet_id is set bet_sub_id is useless
        :param winnings: specifies the win amount. If winnings = 0 the bet is considered to be lost.
        :param refund: specifies refund value. If value is set bet is considered to be canceled.
                       If winnings is set bet will be not canceled so this parameter is useless.
        :param submit_name: specifies action should be applied to the bet. 'StlBet' goes for settling the bet,
                            'CancelBet' goes for canceling the bet.
        """
        url = self.admin
        if not bet_id:
            bet_id = self.get_lotto_bet_id(sub_id=bet_sub_id)
        params = (
            ('Manual', ''),
            ('BetWinnings', winnings),
            ('BetWinningsTax', '0'),
            ('BetRefund', refund),
            ('BetComment', ''),
            ('BetId', bet_id),
            ('SubmitName', submit_name),
            ('action', 'ADMIN::BET::DoXGameManualSettle')
        )
        do_request(url=url, params=params, cookies=self.site_cookies, load_response=False)

    # Auto Test
    def get_autotest_type(self, type_id: str) -> typing.Dict[str, typing.Any]:
        """
        Get autotest configuration for type
        :param type_id: type id
        :return: dict containing various statuses
        """
        url = urljoin(self.site, f'ti/hierarchy/type/{type_id}')

        _logger.debug('request content of the site: %s', url)
        html_text = do_request(url=url, cookies=self.site_cookies, method='GET', load_response=False)

        etree_element = html.fromstring(html_text)
        displayed_el = etree_element.xpath('//div[@id="type_displayed"]')[0]
        active_el = etree_element.xpath('//div[@id="type_status"]')[0]
        min_bet_el = etree_element.xpath('//input[@id="type_ev_min_bet"]')[0]
        max_bet_el = etree_element.xpath('//input[@id="type_ev_max_bet"]')[0]
        live_serv_updates_el=etree_element.xpath('//div[@id="type_push_msg"]')[0]
        cashout_available_el=etree_element.xpath('//div[@id="type_cashout_avail"]')[0]

        return dict(
            displayed = not 'not_displayed' in displayed_el.classes,
            active =  not 'suspended' in active_el.classes,
            min_bet = min_bet_el.value,
            max_bet = max_bet_el.value,
            live_serv_updates = 'selected' in live_serv_updates_el.classes,
            cashout_available = not 'not_avail' in cashout_available_el.classes
        )

    def get_autotest_class(self, class_id: str) -> typing.Dict[str, bool]:
        """
        Gets autotest configuration for class
        :param class_id: class id
        :return: dict containing various statuses
        """
        url = urljoin(self.site, f'ti/hierarchy/class/{class_id}')

        _logger.debug('request content of the site: %s', url)
        html_text = do_request(url=url, cookies=self.site_cookies, method='GET', load_response=False)

        etree_element = html.fromstring(html_text)
        displayed_el = etree_element.xpath('//div[@id="class_displayed"]')[0]
        active_el = etree_element.xpath('//div[@id="class_status"]')[0]
        live_serv_updates_el=etree_element.xpath('//div[@id="class_push_msg"]')[0]
        cashout_available_el=etree_element.xpath('//div[@id="class_cashout_avail"]')[0]

        return dict(
            displayed = not 'not_displayed' in displayed_el.classes,
            active =  not 'suspended' in active_el.classes,
            live_serv_updates = 'selected' in live_serv_updates_el.classes,
            cashout_available = not 'not_avail' in cashout_available_el.classes
        )

    def get_bet_info(self, username: str, bet_id: str, **kwargs):
        """
        Get information about bet from TI

        :param username: username
        :param bet_id: bet id
        :return: named tuple with information about bet
        """
        params = (
            ('action', 'bet::search::H_search'),
            ('submit_search', ''),
            ('search_type', 'S'),
            ('last_n', '100'),
            ('placed_date_range', 'L7D'),
            ('channel_list', '@ B C D E F G H I J K L M N O P Q R S T U V W X Y Z e f p t y z'),
            ('channel_changed_trigger', '0'),
            ('receipt', bet_id),
            ('term_code', ''),
            ('username', username),
            ('username_exact', 'Y'),
            ('acct_no', ''),
            ('acct_no_exact', 'Y'),
            ('stake_min', ''),
            ('stake_max', ''),
            ('stake_factor_min', ''),
            ('stake_factor_max', ''),
            ('winnings_min', ''),
            ('winnings_max', ''),
            ('potential_payout_min', ''),
            ('potential_payout_max', ''),
            ('bir', '-'),
            ('price_type', ''),
            ('hcap_value', ''),
            ('leg_type_W', 'N'),
            ('leg_type_P', 'N'),
            ('leg_type_E', 'N'),
            ('leg_type_L', 'N'),
            ('leg_type_I', 'N'),
            ('leg_type_Q', 'N'),
            ('leg_type_list', 'W P E L I Q'),
            ('exotic', ''),
            ('bir_index', ''),
            ('dd_id', ''),
            ('dd_level', ''),
            ('ev_mkt_ids', ''),
            ('ev_oc_ids', ''),
            ('exclude_bets_L', 'N'),
            ('exclude_bets_V', 'N'),
            ('exclude_bets_W', 'N'),
            ('results_type_SGL', 'Y'),
            ('results_type_MUL', 'Y'),
            ('results_type_MAN', 'N'),
            ('results_types', ''),
            ('settled', '-'),
            ('bet_hist_reason', '-'),
            ('disp_bet_hist', ''),
            ('settled_at_date_range', '-'),
            ('fname', ''),
            ('fname_exact', 'Y'),
            ('lname', ''),
            ('lname_exact', 'Y'),
            ('cust_id', ''),
            ('search_bet_ipaddress', ''),
            ('search_bet_ipaddress_exact', 'Y'),
            ('refunds_min', ''),
            ('refunds_max', ''),
            ('total_returns', ''),
            ('grpd_bet_id', ''),
            ('grpd_bet_type', 'N'),
            ('barcode', ''),
            ('leg_sort_list', '-- AH WH OU HL hl MH SF RF QN CF TC F4 OT O4 OQ CQ SC FW LW AW CW MP ES'),
            ('leg_sort_changed_trigger', '0'),
            ('market_sort_list', ''),
            ('market_sort_changed_trigger', '0'),
            ('acct_type', '-'),
            ('bet_type_list', 'SGL DBL SS2 DS2 TBL TRX ROB 3BY4 PAT DS3 SS3 LY6 ACC4 LY10 YAP 4BY5 L15 LY11 DS4 FLG YAN'
                              ' SS4 DS5 SS5 ACC5 FSP L31 CAN SS6 PON HNZ ACC6 L63 DS6 SHNZ MAG7 DS7 SS7 L7B ACC7 DS8 '
                              'SS8 ACC8 GOL DS9 UJK SS9 ACC9 AC10 SS10 DS10 AC11 DS11 SS11 AC12 P612 P712 P512 SS12 DS12 '
                              'P613 DS13 P713 AC13 SS13 P513 P413 P813 P913 DS14 SS14 P1014 P414 P514 AC14 P914 DS15 '
                              'P1115 P415 AC15 SS15 P1216 P416 AC16 P1317 P417 AC17 P1518 AC18 AC19 P1619 P1720 AC20 '
                              'P1821 AC21 AC22 P1922 P2023 AC23 AC24 P2124 AC25 P2225'),
            ('bet_type_changed_trigger', '0'),
            ('status_A', 'Y'),
            ('status_C', 'N'),
            ('status_P', 'Y'),
            ('status_S', 'Y'),
            ('status_X', 'N'),
            ('status_list', 'A C P S X'),
            ('ignore_unrestricted_bets', 'N'),
            ('funding_method_cash', 'Y'),
            ('funding_method_token', 'Y'),
            ('funding_method_partial', 'Y'),
            ('is_off_time', 'N'),
            ('page_no', '0'),
            ('sort_col', ''),
            ('sort_dir', ''),
            ('sort_type', '')
        )

        r = do_request(url=self.site, params=params, cookies=self.site_cookies, load_response=False)
        page = html.fromstring(r)
        stake = page.xpath('//span[contains(@id, "bet_search_stake_per_line")]')[0].text
        est_returns = page.xpath('//span[contains(@id, "bet_search_potential_payout")]')[0].text
        events = [re.sub(r'\|\n|\t', '', event.text) for event in page.xpath('//a[contains(@href, "/ti/fieldbook/event/")]')]
        bets = [re.sub(r'\|\n|\t', '', event.text) for event in page.xpath('//a[contains(@href, "/ti/fieldbook/selection/")]')]
        markets = [re.sub(r'\|\n|\t', '', event.text) for event in page.xpath('//a[contains(@href, "/ti/fieldbook/market/")]')]
        BetInfo = namedtuple('bet_information', ['stake', 'est_returns', 'events', 'bets', 'markets'])
        bet_info = BetInfo(stake, est_returns, events, bets, markets)
        return bet_info

    def overask_stake_config_items(self) -> tuple:
        """
        Get the information about overask stake amount and factor
        :return: returns the overask stake items(amount and factor)
        """
        url = self.admin
        params = '?action=ADMIN::OPENBET_CFG::GoOpenbetCfgList&CfgGrpName=Overask'
        html_text = do_request(url=url + params, cookies=self.site_cookies, method='GET', load_response=False)
        etree_element = html.fromstring(html_text)
        amount_selector = '//input[@name="CfgValue_0"]'
        factor_selector = '//input[@name="CfgValue_1"]'
        amount_element = etree_element.xpath(amount_selector)
        factor_element = etree_element.xpath(factor_selector)
        if not amount_element and not factor_element:
            raise OBException('cannot get OVERASK_STAKE_AMOUNT and OVERASK_STAKE_FACTOR')
        overask_stake_items = (float(amount_element[0].value), float(factor_element[0].value))
        return overask_stake_items

    def create_fanzone_league_event_id(self, league_id, home_team, away_team,
                                       home_team_external_id, away_team_external_id, **kwargs):
        """
        Create the Fanzone Event
        :param league_id: Type ID of the league
        :param home_team: Home Team name of the event
        :param away_team: Away Team name of the event
        :param home_team_external_id: Home Team External ID
        :param away_team_external_id: Away Team External ID
        :return: returns the EventID, MarketID, SelectionId's of the created Fanzone event
        """
        result = {}
        current_time = str(datetime.datetime.utcnow())
        current_date = datetime.datetime.strptime(current_time.split(".")[0], "%Y-%m-%d %H:%M:%S")
        start_time = str(current_date + datetime.timedelta(days=1))
        ats_data = '''<?xml version="1.0" encoding="UTF-8"?>
                <oxiFeedRequest version="1.0">
                <auth username="'''+self.user+'''" password="'''+self.password+'''"/>
                <eventInsert>
                <typeId>
                <openbetId>'''+str(league_id)+'''</openbetId>
                </typeId>
                <eventId>
                <externalId>'''+home_team+''' vs '''+away_team+ current_time.split(".")[1]+'''</externalId>
                </eventId>
                <eventName>'''+home_team+''' vs '''+away_team+ current_time.split(".")[1]+'''</eventName>
                <startTime>'''+ kwargs.get('start_date', start_time)+'''</startTime>
                <eventSort>match</eventSort>
                <status>'''+ kwargs.get('event_status', "active")+'''</status>
                <display displayed="yes" />
                <!-- Home Team -->
                <teamInsert>
                <teamId>
                <externalId>'''+home_team_external_id+'''</externalId>
                </teamId>
                <teamName>'''+home_team+'''</teamName>
                <teamLocation>home</teamLocation>
                </teamInsert>
                <!-- Away Team -->
                <teamInsert>
                <teamId>
                <externalId>'''+away_team_external_id+'''</externalId>
                </teamId>
                <teamName>'''+away_team+'''</teamName>
                <teamLocation>away</teamLocation>
                </teamInsert>
                </eventInsert>
                </oxiFeedRequest>'''
        headers = {'Content-Type': 'application/xml'}
        try:
            response = do_request(method='POST',
                       url=self.football_config.fanzone_hostname,
                       headers=headers,
                       data=ats_data, cookies=self.site_cookies,load_response=False)
            convert_xml_to_dict = xmltodict.parse(response)
            eventID = convert_xml_to_dict['oxiFeedResponse']['eventInsert']['eventId']['openbetId']
        except:
            raise Exception(f'Event is not created for the teams {home_team} vs {away_team}')
        self.CREATED_EVENTS.append(eventID)
        self.update_event_name(eventID, event_name=home_team+" vs "+away_team)
        event = CreateSportEvent(env=self.env, brand=self.brand, category_id=self.football_config.category_id,
                                 class_id=self.football_config.autotest_class.class_id,
                                 type_id=self.football_config.autotest_class.autotest_premier_league.type_id)
        market_name= self.football_config.default_market_name.replace('|', '')
        template_id= self.football_config.autotest_class.autotest_premier_league.market_template_id
        try:
            market_id = event.create_market(event_id=eventID, market_name=market_name, market_template_id=template_id)
        except:
            raise OBException(f'Market is not added to evnet id {eventID}')
        try:
            selection_ids = event.add_selections(prices=event.other_sport_prices, marketID=market_id,
                                  selection_names=('|'+home_team+'|', '|'+away_team+'|'),
                                  selection_types=('H', 'A'), **kwargs)
        except:
            raise OBException(f'Selections were not added to market id {market_id} for event {eventID}')
        result['eventID']=eventID
        result['market_id']=market_id
        result['Selection_ids']=selection_ids
        return result

    def map_fanzone_event_selection_id(self, selection_id, fanzone_team, team_external_id):
        """
        Map the autright event Selection ID
        :param selection_id: Selection ID of the fanzone event
        :param fanzone_team: Fanzone Team name of the event
        :param team_external_id: Fanzone Team External ID
        :return: response of the mapped selection ID
        """
        ats_data = '''<oxiFeedRequest version="1.0" timestamp="2015-11-30 13:22:08">
                    <auth username="'''+self.user+'''" password="'''+self.password+'''" current_uname=""/>
                    <selectionTeamInsert>
                    <selectionId>
                    <openbetId>'''+selection_id+'''</openbetId>
                    <externalId>'''+fanzone_team+'''</externalId>
                    </selectionId>
                    <teamId>
                    <externalId>'''+team_external_id+'''</externalId>
                    </teamId>
                    </selectionTeamInsert>
                    </oxiFeedRequest>'''
        headers = {'Content-Type': 'application/xml'}
        response = do_request(method='POST',
                  url=self.football_config.fanzone_hostname,
                  headers=headers,
                  data=ats_data, cookies=self.site_cookies,load_response=False)
        return response

    def update_event_name(self, eventID, event_name):
        """
        Update Event Name
        :param eventID: event id
        :param event_name: new event name
        """
        params = '?action=hierarchy::event::H_update&id={0}&name={1}&exact_flags=Y'.format(eventID, event_name)
        url = self.site + params
        do_request(url=url, cookies=self.site_cookies)


if __name__ == '__main__':
    ob = OBConfig(env='tst2', brand='ladbrokes')
