from collections import namedtuple


class Coupons(object):
    """
    src/app/sb/components/couponsList/coupons-list.constant.ts
    """
    POPULAR_COUPONS = 'Popular Coupons'
    GOALSCORER_COUPON = 'Goalscorer Coupon'

    _expected_coupon_markets = namedtuple('coupon_markets', ('match_result', 'both_teams_to_score',
                                                             'total_goals_over_under_1_5', 'over_under_total_goals',
                                                             'score_goal_in_both_halves', 'draw_no_bet',
                                                             'first_half_result', 'to_win_to_nil',
                                                             'match_result_and_both_teams_to_score'))
    EXPECTED_COUPON_MARKET_TEMPLATES_NAMES = _expected_coupon_markets(match_result='Match Result',
                                                                      both_teams_to_score='Both Teams to Score',
                                                                      total_goals_over_under_1_5='Total Goals Over/Under 1.5',
                                                                      over_under_total_goals='Total Goals Over/Under 1.5',
                                                                      score_goal_in_both_halves='Goal in Both Halves',
                                                                      draw_no_bet='Draw No Bet',
                                                                      first_half_result='1st Half Result',
                                                                      to_win_to_nil='To Win To Nil',
                                                                      match_result_and_both_teams_to_score='Match Result & Both Teams To Score')
    # Football Coupons
    COUPONS_TITLE = 'COUPONS'
    COUPON_TIME_HEADER = 'Today'
    SHOW_MORE = 'Show More'
    SEE_ALL = 'See All'
