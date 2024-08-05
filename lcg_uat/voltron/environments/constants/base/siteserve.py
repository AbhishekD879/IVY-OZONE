# todo:     VOL-4858 [SiteServe] Get constants from SS response
from collections import namedtuple


class SiteServe(object):
    AUTO_TEST_LEAGUE = 'AUTO TEST LEAGUE'
    AUTO_TEST_AUTO_TEST_LEAGUE = 'Auto Test - Auto Test League'

    # Austrian volleyball league name
    VOLLEYBALL_LEAGUE = 'AVL'

    # America football league name
    NCCA = 'NCAA'
    NCCA_BOWLS = 'NCAA Bowls'

    # football league names
    PREMIER_LEAGUE_NAME = 'Premier League'
    AUTO_TEST_PREMIER_LEAGUE_NAME = 'Autotest Premier League'
    LALIGA = 'Spanish La Liga'
    CHAMPIONSHIP = 'Championship'

    # countries
    ENGLAND = 'ENGLAND'
    SPAIN = 'SPAIN'

    # sport league names
    SNOOKER_LEAGUE_NAME = 'WORLD CHAMPIONSHIP'
    CLUB_FOOTBALL_LEAGUE = 'CLUB FOOTBALL'
    BASEBALL_LEAGUE_NAME = 'AUTO TEST LEAGUE'
    AHL_LEAGUE_NAME = 'AHL'
    CRICKET_LEAGUE_NAME = 'CRICKET AUTOTEST'

    POOLS_TYPES_CODES = {'uk_tote_win': 'UWIN', 'uk_tote_place': 'UPLC', 'uk_tote_exacta': 'UEXA',
                         'uk_tote_trifecta': 'UTRI', 'uk_tote_quadpot': 'UQDP', 'uk_tote_placepot': 'UPLP',
                         'uk_tote_jackpot': 'UJKP', 'uk_tote_scoop6': 'USC6'}
    INT_POOLS_TYPES_CODES = {'int_tote_win': 'WN', 'int_tote_place': 'PL', 'int_tote_exacta': 'EX',
                             'int_tote_trifecta': 'TR', 'int_tote_show': 'SH'}

    EUROPEAN_OPEN_LEAGUE = 'EUROPEAN OPEN'

    OUTRIGHT_EVENT_SORT_CODES = 'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20'

    # Sport tabs
    TENNIS_TAB = 'TENNIS'
    FOOTBALL_TAB = 'FOOTBALL'
    HANDBALL_TAB = 'HANDBALL'
    BASKETBALL_TAB = 'BASKETBALL'
    VOLLEYBALL_ACCORDION = 'VOLLEYBALL'
    BEACH_VOLLEYBALL = 'BEACH VOLLEYBALL'
    IN_PLAY_TAB = 'IN-PLAY'  # todo VOL-4885
    SNOOKER_TAB = 'SNOOKER'
    GOLF_TAB = 'GOLF'

    EXPECTED_COUPON_NAME = 'Football Auto Test Coupon'
    BASKETBALL_COUPON_NAME_1 = 'Basketball Auto Test Coupon'
    TENNIS_COUPON_NAME = 'Tennis Auto Test Coupon'

    _expected_market_tab_keys = namedtuple('expected_market_tab_keys',
                                           ['all_markets', 'main', 'main_markets', 'goal_markets', 'game_markets',
                                            'game', 'other_markets', 'autotest_collection', 'build_your_bet',
                                            'current_game_1st_point', 'set_1_game_1_deuce', 'yourcall', 'five_a_side'])
    EXPECTED_MARKET_TABS = _expected_market_tab_keys(all_markets='ALL MARKETS',
                                                     main='MAIN',
                                                     main_markets='MAIN MARKETS',
                                                     goal_markets='GOAL MARKETS',
                                                     game_markets='GAME MARKETS',
                                                     game='GAME',
                                                     other_markets='OTHER MARKETS',
                                                     autotest_collection='AUTOTEST COLLECTION',
                                                     build_your_bet='BUILD YOUR BET',
                                                     current_game_1st_point='CURRENT GAME 1ST POINT',
                                                     set_1_game_1_deuce='SET 1 GAME 1 DEUCE',
                                                     yourcall='#YOURCALL',
                                                     five_a_side='5-A-SIDE')

    _expected_markets = namedtuple('expected_markets', ('main_markets', 'match_result', 'both_teams_to_score', 'next_team_to_score',
                                                        'total_goals_over_under_1_5', 'over_under_total_goals', 'total_goals',
                                                        'score_goal_in_both_halves', 'draw_no_bet',
                                                        'match_result_and_both_teams_to_score',
                                                        'first_half_result', 'to_win_to_nil', 'to_win_not_to_nil',
                                                        'extra_time_result', 'penalty_shoot_out_winner', 'to_qualify',
                                                        'match_betting', 'total_goals_over_under_2_5',
                                                        'total_goals_over_under_3_5', 'total_goals_over_under_4_5',
                                                        'match_result_default', 'three_ball_betting', 'two_ball_betting',
                                                        'money_line', 'sixty_minutes_betting', 'puck_line',
                                                        'total_goals_2_way', 'total_points', 'handicap_2_way',
                                                        'home_team_total_points', 'away_team_total_points',
                                                        'half_total_points', 'quarter_total_points',
                                                        'most_180s', 'total_180s_over_under', 'handicap', 'match_set_handicap',
                                                        'total_match_points', 'fight_betting', 'rugby_handicap', 'total_sixes',
                                                        'next_over_runs', 'team_runs', 'runs_at_fall_of_next_wicket',
                                                        'spread', 'sixty_minute_betting', 'half_time_full_time','two_up_Instant_Win',
                                                        'no_draw_handicap_1', 'no_draw_handicap_2', 'no_draw_handicap_3', 'Handicap_Betting'))

    EXPECTED_MARKETS_NAMES = _expected_markets(match_result='Match Result',
                                               both_teams_to_score='Both Teams to Score',
                                               next_team_to_score='Next Team to Score',
                                               extra_time_result='Extra Time Result',
                                               total_goals_over_under_1_5='Total Goals Over/Under 1.5',
                                               total_goals_over_under_2_5='Total Goals Over/Under 2.5',
                                               total_goals_over_under_3_5='Total Goals Over/Under 3.5',
                                               total_goals_over_under_4_5='Total Goals Over/Under 4.5',
                                               over_under_total_goals='Total Goals Over/Under 1.5',
                                               total_goals='Total Goals',
                                               score_goal_in_both_halves='Score Goal in Both Halves',
                                               match_result_and_both_teams_to_score='Match Result & Both Teams To Score',
                                               draw_no_bet='Draw No Bet',
                                               first_half_result='1st Half Result',
                                               to_win_to_nil='To Win To Nil',
                                               to_win_not_to_nil='To Win & Both Teams to Score',
                                               penalty_shoot_out_winner='Penalty Shoot-Out Winner',
                                               to_qualify='To Qualify',
                                               main_markets='Main Markets',
                                               match_betting='Match Betting',
                                               match_result_default='Match Result',
                                               three_ball_betting='3 Ball Betting',
                                               two_ball_betting='2 Ball Betting',
                                               money_line='Money Line',
                                               sixty_minutes_betting='60 Minutes Betting',
                                               sixty_minute_betting='60 Minute Betting',
                                               puck_line='Puck Line',
                                               total_goals_2_way='Total Goals 2-way',
                                               total_points='Total Points',
                                               handicap_2_way='Handicap',
                                               spread='Spread',
                                               home_team_total_points='Home Team Total Points',
                                               away_team_total_points='Away Team Total Points',
                                               half_total_points='Current Half Total Points',
                                               quarter_total_points='Current Quarter Total Points',
                                               most_180s='Most 180s',
                                               total_180s_over_under='Total 180s',
                                               handicap='Handicap',
                                               match_set_handicap='Set Handicap',
                                               total_match_points='Total Points',
                                               fight_betting='Fight Betting',
                                               rugby_handicap='Handicap',
                                               total_sixes='Total Sixes',
                                               next_over_runs='Next Over Runs',
                                               team_runs='Team Runs',
                                               runs_at_fall_of_next_wicket='Runs at Fall of Next Wicket',
                                               half_time_full_time='Half-Time/Full-Time',
                                               two_up_Instant_Win='2Up - Instant Win',
                                               no_draw_handicap_1='No Draw Handicap 1',
                                               no_draw_handicap_2='No Draw Handicap 2',
                                               no_draw_handicap_3='No Draw Handicap 3',
                                               Handicap_Betting='Handicap Betting')

    _expected_market_section_keys = namedtuple('expected_market_section_keys',
                                               ['match_result_and_both_teams_to_score',
                                                'goals_to_be_scored', 'first_and_second_half_result', 'draw_no_bet',
                                                'match_result', 'outright', 'correct_score',
                                                'scorecast', 'handicap_results',
                                                'popular_goalscorer_markets',
                                                'other_goalscorer_markets', 'yourcall_specials_football',
                                                'yourcall_specials', 'yourcall', 'extra_time_result',
                                                'over_under_total_goals', 'total_goals', 'match_betting',
                                                'player_bets', 'player_total_passes', 'player_total_goals', 'both_teams_to_score', 'over_under_goals',
                                                'over_under_corners', 'over_under_booking_points',
                                                'player_to_be_carded', 'anytime_goalscorer', 'double_chance',
                                                'to_win_not_to_nil', 'to_qualify',
                                                'both_teams_to_score_in_both_halves',
                                                'player_to_score_2plus_goals', 'money_line', 'to_win_to_nil',
                                                'spread', 'sixty_minute_betting', 'total_points', 'handicap',
                                                'total_frames', 'total_runs', 'run_line', 'total_goals_odd_even',
                                                'first_half_correct_score', 'second_half_correct_score', 'frame_x_winner',
                                                'two_up_Instant_Win', 'no_draw_handicap_1', 'no_draw_handicap_2', 'no_draw_handicap_3', 'Handicap_Betting'
                                                ]
                                               )
    EXPECTED_MARKET_SECTIONS = _expected_market_section_keys(
        match_result_and_both_teams_to_score='MATCH RESULT & BOTH TEAMS TO SCORE',
        goals_to_be_scored='GOAL TO BE SCORED',
        first_and_second_half_result='1ST HALF / 2ND HALF RESULT', draw_no_bet='DRAW NO BET',
        match_result='MATCH RESULT', outright='OUTRIGHT', correct_score='CORRECT SCORE', scorecast='SCORECAST',
        handicap_results='HANDICAP RESULTS', popular_goalscorer_markets='POPULAR GOALSCORER MARKETS',
        other_goalscorer_markets='OTHER GOALSCORER MARKETS', yourcall_specials_football='#YOURCALL SPECIALS FOOTBALL',
        yourcall_specials='#YOURCALL SPECIALS FOOTBALL', yourcall='#YOURCALL',
        extra_time_result='EXTRA-TIME RESULT', over_under_goals='OVER/UNDER GOALS',
        over_under_total_goals='OVER/UNDER TOTAL GOALS', total_goals='TOTAL GOALS', match_betting='MATCH BETTING', player_bets='PLAYER BETS',
        player_total_passes='PLAYER TOTAL PASSES', player_total_goals='PLAYER TOTAL GOALS', both_teams_to_score='BOTH TEAMS TO SCORE', over_under_corners='OVER/UNDER CORNERS',
        over_under_booking_points='OVER/UNDER BOOKING POINTS', player_to_be_carded='PLAYER TO BE CARDED',
        anytime_goalscorer='ANYTIME GOALSCORER', double_chance='DOUBLE CHANCE', to_win_not_to_nil='TO WIN NOT TO NIL',
        to_qualify='TO QUALIFY', both_teams_to_score_in_both_halves='BOTH TEAMS TO SCORE IN BOTH HALVES',
        player_to_score_2plus_goals='PLAYER TO SCORE 2+ GOALS', money_line='MONEY LINE', to_win_to_nil='TO WIN TO NIL',
        spread='SPREAD', sixty_minute_betting='60 MINUTE BETTING', total_points='TOTAL POINTS', handicap='HANDICAP',
        total_frames='TOTAL FRAMES', total_runs='TOTAL RUNS', run_line='RUN LINE', total_goals_odd_even='TOTAL GOALS ODD/EVEN',
        first_half_correct_score='FIRST HALF CORRECT SCORE', second_half_correct_score='SECOND HALF CORRECT SCORE',
        frame_x_winner="Frame X Winner",two_up_Instant_Win='2Up - Instant Win',
        no_draw_handicap_1='No Draw Handicap 1', no_draw_handicap_2='No Draw Handicap 2',
        no_draw_handicap_3='No Draw Handicap 3', Handicap_Betting='Handicap Betting')

    EXPECTED_MARKET_SECTIONS_TITLE = _expected_market_section_keys(
        match_result_and_both_teams_to_score=EXPECTED_MARKET_SECTIONS.match_result_and_both_teams_to_score.title(),
        goals_to_be_scored=EXPECTED_MARKET_SECTIONS.goals_to_be_scored.title(),
        draw_no_bet=EXPECTED_MARKET_SECTIONS.draw_no_bet.title(),
        first_and_second_half_result=EXPECTED_MARKET_SECTIONS.first_and_second_half_result.title(),
        match_result=EXPECTED_MARKET_SECTIONS.match_result.title(),
        outright=EXPECTED_MARKET_SECTIONS.outright.title(),
        correct_score=EXPECTED_MARKET_SECTIONS.correct_score.title(),
        scorecast=EXPECTED_MARKET_SECTIONS.scorecast.title(),
        handicap_results=EXPECTED_MARKET_SECTIONS.handicap_results.title(),
        popular_goalscorer_markets=EXPECTED_MARKET_SECTIONS.popular_goalscorer_markets.title(),
        other_goalscorer_markets=EXPECTED_MARKET_SECTIONS.other_goalscorer_markets.title(),
        yourcall_specials_football=EXPECTED_MARKET_SECTIONS.yourcall_specials_football.title(),
        yourcall_specials=EXPECTED_MARKET_SECTIONS.yourcall_specials_football.title(),
        yourcall=EXPECTED_MARKET_SECTIONS.yourcall.title(),
        extra_time_result=EXPECTED_MARKET_SECTIONS.extra_time_result.title(),
        over_under_goals=EXPECTED_MARKET_SECTIONS.over_under_goals.title(),
        over_under_total_goals=EXPECTED_MARKET_SECTIONS.over_under_total_goals.title(),
        total_goals=EXPECTED_MARKET_SECTIONS.total_goals.title(),
        match_betting=EXPECTED_MARKET_SECTIONS.match_betting.title(),
        player_bets=EXPECTED_MARKET_SECTIONS.player_bets.title(),
        player_total_passes=EXPECTED_MARKET_SECTIONS.player_total_passes.title(),
        player_total_goals=EXPECTED_MARKET_SECTIONS.player_total_goals.title(),
        both_teams_to_score=EXPECTED_MARKET_SECTIONS.both_teams_to_score.title(),
        over_under_corners=EXPECTED_MARKET_SECTIONS.over_under_corners.title(),
        over_under_booking_points=EXPECTED_MARKET_SECTIONS.over_under_booking_points.title(),
        player_to_be_carded=EXPECTED_MARKET_SECTIONS.player_to_be_carded.title(),
        anytime_goalscorer=EXPECTED_MARKET_SECTIONS.anytime_goalscorer.title(),
        double_chance=EXPECTED_MARKET_SECTIONS.double_chance.title(),
        to_win_not_to_nil=EXPECTED_MARKET_SECTIONS.to_win_not_to_nil.title(),
        to_qualify=EXPECTED_MARKET_SECTIONS.to_qualify.title(),
        both_teams_to_score_in_both_halves=EXPECTED_MARKET_SECTIONS.both_teams_to_score_in_both_halves.title(),
        player_to_score_2plus_goals=EXPECTED_MARKET_SECTIONS.player_to_score_2plus_goals.title(),
        money_line=EXPECTED_MARKET_SECTIONS.money_line.title(),
        to_win_to_nil=EXPECTED_MARKET_SECTIONS.to_win_to_nil.title(),
        spread=EXPECTED_MARKET_SECTIONS.spread.title(),
        sixty_minute_betting=EXPECTED_MARKET_SECTIONS.sixty_minute_betting.title(),
        total_points=EXPECTED_MARKET_SECTIONS.total_points.title(),
        handicap=EXPECTED_MARKET_SECTIONS.handicap.title(),
        total_frames=EXPECTED_MARKET_SECTIONS.total_frames.title(),
        total_runs=EXPECTED_MARKET_SECTIONS.total_runs.title(),
        run_line=EXPECTED_MARKET_SECTIONS.run_line.title(),
        total_goals_odd_even=EXPECTED_MARKET_SECTIONS.total_goals_odd_even.title(),
        first_half_correct_score=EXPECTED_MARKET_SECTIONS.first_half_correct_score.title(),
        second_half_correct_score=EXPECTED_MARKET_SECTIONS.second_half_correct_score.title(),
        frame_x_winner=EXPECTED_MARKET_SECTIONS.frame_x_winner.title(),
        two_up_Instant_Win=EXPECTED_MARKET_SECTIONS.two_up_Instant_Win.title(),
        no_draw_handicap_1=EXPECTED_MARKET_SECTIONS.no_draw_handicap_1.title(),
        no_draw_handicap_2=EXPECTED_MARKET_SECTIONS.no_draw_handicap_2.title(),
        no_draw_handicap_3=EXPECTED_MARKET_SECTIONS.no_draw_handicap_3.title(),
        Handicap_Betting=EXPECTED_MARKET_SECTIONS.Handicap_Betting.title(),
    )
    OUTRIGHT = 'Outright'
