markets = [
    ('total_goals', {'cashout': True}),
    ('next_team_to_score', {'cashout': True}),
    ('extra_time_result', {'cashout': True}),
    ('both_teams_to_score', {'cashout': True}),
    ('to_win_not_to_nil', {'cashout': True}),
    ('draw_no_bet', {'cashout': True}),
    ('first_half_result', {'cashout': True}),
    ('to_qualify', {'cashout': True}),
    ('penalty_shoot_out_winner', {'cashout': True})
]

extended_markets = [
    ('over_under_total_goals', {'cashout': True, 'over_under': 1.5}),
    ('over_under_total_goals', {'cashout': True, 'over_under': 2.5}),
    ('over_under_total_goals', {'cashout': True, 'over_under': 3.5}),
    ('over_under_total_goals', {'cashout': True, 'over_under': 4.5}),
    ('match_result_and_over_under_2_5_goals', {'cashout': True, 'over_under': 2.5}),
    ('match_result_and_over_under_3_5_goals', {'cashout': True, 'over_under': 3.5}),
    ('match_result_and_over_under_4_5_goals', {'cashout': True, 'over_under': 4.5}),
    ('match_result_and_over_under_5_5_goals', {'cashout': True, 'over_under': 5.5}),
    ('match_result_and_over_under_6_5_goals', {'cashout': True, 'over_under': 6.5}),
    ('match_result_and_over_under_7_5_goals', {'cashout': True, 'over_under': 7.5}),
    ('match_result_and_over_under_8_5_goals', {'cashout': True, 'over_under': 8.5}),
    ('match_result_and_over_under_9_5_goals', {'cashout': True, 'over_under': 9.5}),
    ('both_team_to_score_and_over_under_2_5_goals', {'cashout': True, 'over_under': 2.5}),
    ('both_team_to_score_and_over_under_3_5_goals', {'cashout': True, 'over_under': 3.5}),
    ('both_team_to_score_and_over_under_4_5_goals', {'cashout': True, 'over_under': 4.5}),
    ('both_team_to_score_and_over_under_5_5_goals', {'cashout': True, 'over_under': 5.5}),
    ('both_team_to_score_and_over_under_6_5_goals', {'cashout': True, 'over_under': 6.5}),
    ('both_team_to_score_and_over_under_7_5_goals', {'cashout': True, 'over_under': 7.5}),
    ('both_team_to_score_and_over_under_8_5_goals', {'cashout': True, 'over_under': 8.5}),
    ('both_team_to_score_and_over_under_9_5_goals', {'cashout': True, 'over_under': 9.5}),
]

event_types = [
    'add_autotest_premier_league_football_event',
    'add_football_event_to_spanish_la_liga',
    'add_football_event_to_england_premier_league',
    'add_football_event_to_italy_serie_a',
    'add_football_event_to_uefa_champions_league',
    'add_football_event_to_autotest_league2',
    'add_tennis_event_to_autotest_trophy',
    'add_baseball_event_to_autotest_league',
    'add_baseball_event_to_us_league',
    'add_american_football_event_to_autotest_league',
    'add_autotest_premier_league_football_outright_event',
    'add_england_premier_league_football_outright_event'
]


def get_next_event_type():
    """
    rotates event types by returning first value of the list and appending it to end of the list
    :return: ob_client event type method name
    :rtype: str
    """
    event_type = event_types.pop(0)
    event_types.append(event_type)
    return event_type
