from crlat_ob_client.openbet_config import OBConfig

BRAND = 'bma'
ENV = 'tst2'

ob = OBConfig(brand=BRAND, env=ENV)

ob.add_autotest_premier_league_football_event(markets=[
    ('handicap', {'cashout': True}),  # handicap_match_result, handicap_first_half , handicap_second_half
    ('scorecast', {'cashout': True}),  # correct_score, first_goalscorer, last_goalscorer,
                                       #  first_goal_scorecast, last_goal_scorecast
    ('both_teams_to_score', {'cashout': True}),
    ('match_result_and_both_teams_to_score', {'cashout': True}),
    ('over_under_total_goals', {'cashout': True, 'over_under': 2.5}),
    ('total_goals', {'cashout': True}),
    ('to_qualify', {'cashout': True}),
    ('to_win_to_nil', {'cashout': True}),
    ('to_win_not_to_nil', {'cashout': True}),
    ('first_half_result', {'cashout': True}),
    ('draw_no_bet', {'cashout': True}),
    ('next_team_to_score', {'cashout': True}),
    ('extra_time_result', {'cashout': True}),
    ('anytime_goalscorer', {'cashout': True}),
    ('score_goal_in_both_halves', {'cashout': True}),
    ('goalscorer_2_or_more', {'cashout': True}),
    ('hat_trick', {'cashout': True}),
    ('your_call', {'cashout': True}),
    ('penalty_shoot_out_winner', {'cashout': True}),
    ('double_chance', {'cashout': True}),
    ('half_time_double_chance', {'cashout': True}),
    ('second_half_double_chance', {'cashout': True}),
    ('over_under_second_half', {'cashout': True}),
    ('over_under_first_half', {'cashout': True}),
    ('match_result_and_over_under', {'cashout': True}),
    ('both_team_to_score_and_over_under', {'cashout': True}),
])


for event in ob.CREATED_EVENTS:
    ob.change_event_state(event_id=event, displayed=False, active=False)
