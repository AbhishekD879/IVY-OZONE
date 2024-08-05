### What is this repository for? ###

**The Repository is for creating LIVE/UPCOMING events and LIVE UPDATES for**

#### SUPPORTED LEAGUES:

    FOOTBALL
    * Football Autotest Premier league
    * Football Spanish La Liga league
    * Football England Premier league
    * Football Italy Serie A league
    * Football UEFA Champions league
    * Football Autotest League 2 league
    
    TENNIS
    * Tennis Autotest Trophy league
    
    BASEBALL
    * Baseball Autotest league
    * Baseball US league
    
    AMERICAN FOOTBALL
    * American football Autotest league
    
    OUTRIGHT FOOTBALL
    * Outright Football Autotest Premier league
    * Outright Football England Premier league
    
#### SUPPORTED MARKETS:

```
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
```

It is possibility to create **'add_autotest_premier_league_football_event'** with wide number of custom markets:

```yaml
        autotest_premier_league:
          type_id:  3756
          market_template_id: 552754
          market_name: '|Match Result|'
          outright_market_template_id: 563471
          outright_market_name: '|Outright|'
          markets:
            default:
              '|Default|': 581449
            handicap_match_result:
              '|Handicap Match Result _placeholder_|': 562391
            handicap_first_half:
              '|Handicap First Half _placeholder_|': 889379
            handicap_second_half:
              '|Handicap Second Half _placeholder_|': 889392
            correct_score:
              '|Correct Score|': 546466
            both_teams_to_score:
              '|Both Teams To Score|': 579346
            match_result_and_both_teams_to_score:
              '|Match Result & Both Teams To Score|': 606101
            over_under_total_goals:
              '|Over/Under Total Goals|': 579347
            total_goals:
              '|Total Goals|': 587592
            to_qualify:
              '|To Qualify|': 579350
            to_win_to_nil:
              '|To Win To Nil|': 606099
            to_win_not_to_nil:
              '|To Win Not To Nil|': 579352
            first_half_result:
              '|First-Half Result|': 579349
            draw_no_bet:
              '|Draw No Bet|': 573814
            next_team_to_score:
              '|Next Team To Score|': 582392
            extra_time_result:
              '|Extra-Time Result|': 940899
            first_goalscorer:
              '|First Goalscorer|': 584663
            first_goal_scorecast:
              '|First Goal Scorecast|': 582750
            anytime_goalscorer:
              '|Anytime Goalscorer|': 599157
            score_goal_in_both_halves:
              '|Score Goal in Both Halves|': 606100
            goalscorer_2_or_more:
              '|Goalscorer - 2 Or More|': 603658
            last_goalscorer:
              '|Last Goalscorer|': 584662
            last_goal_scorecast:
              '|Last Goal Scorecast|': 582751
            hat_trick:
              '|Hat trick|': 583772
            your_call:
              '|YourCallSpecials Market|': 876538
            penalty_shoot_out_winner:
              '|Penalty Shoot-Out Winner|': 939523
            double_chance:
              '|Double Chance|': 889337
            half_time_double_chance:
              '|Half-Time Double Chance|': 889371
            second_half_double_chance:
              '|Second-Half Double Chance|': 889387
            over_under_first_half:
              '|Over/Under First Half|': 889328
            over_under_second_half:
              '|Over/Under Second Half|': 889385
            match_result_and_over_under_2_5_goals:
              '|Match Result and Over/Under 2.5 Goals|': 1624936
            match_result_and_over_under_3_5_goals:
              '|Match Result and Over/Under 3.5 Goals|': 1624937
            match_result_and_over_under_4_5_goals:
              '|Match Result and Over/Under 4.5 Goals|': 1624938
            match_result_and_over_under_5_5_goals:
              '|Match Result and Over/Under 5.5 Goals|': 1624939
            match_result_and_over_under_6_5_goals:
              '|Match Result and Over/Under 6.5 Goals|': 1624940
            match_result_and_over_under_7_5_goals:
              '|Match Result and Over/Under 7.5 Goals|': 1624941
            match_result_and_over_under_8_5_goals:
              '|Match Result and Over/Under 8.5 Goals|': 1624942
            match_result_and_over_under_9_5_goals:
              '|Match Result and Over/Under 9.5 Goals|': 1624943
            match_result_and_over_under_10_5_goals:
              '|Match Result and Over/Under 10.5 Goals|': 1624944
            both_team_to_score_and_over_under_2_5_goals:
              '|Both Teams to Score and Over/Under 2.5 Goals|': 1624945
            both_team_to_score_and_over_under_3_5_goals:
              '|Both Teams to Score and Over/Under 3.5 Goals|': 1624946
            both_team_to_score_and_over_under_4_5_goals:
              '|Both Teams to Score and Over/Under 4.5 Goals|': 1624947
            both_team_to_score_and_over_under_5_5_goals:
              '|Both Teams to Score and Over/Under 5.5 Goals|': 1624948
            both_team_to_score_and_over_under_6_5_goals:
              '|Both Teams to Score and Over/Under 6.5 Goals|': 1624949
            both_team_to_score_and_over_under_7_5_goals:
              '|Both Teams to Score and Over/Under 7.5 Goals|': 1624950
            both_team_to_score_and_over_under_8_5_goals:
              '|Both Teams to Score and Over/Under 8.5 Goals|': 1624951
            both_team_to_score_and_over_under_9_5_goals:
              '|Both Teams to Score and Over/Under 9.5 Goals|': 1624952
            both_team_to_score_and_over_under_10_5_goals:
              '|Both Teams to Score and Over/Under 10.5 Goals|': 1624953

```


### How do I get set up? ###

#### For *Creating Events* run from Terminal:

   ```
   make add_events NUM_OF_EVENTS=0 NUM_OF_PARALLEL_PROCESS=1 ENV=some_env BRAND=some_brand IS_LIVE=True IS_UPCOMING=False ADD_EXTENDED_MARKETS=False EVENT_PREFIX=MQA
   ```
   
   **additional options:**
   
   ```
   IS_ALL_MARKET=True/False
   PERFORM_STREAM=True/False
   IMG_STREAM=True/False
   ```
   
   **E.g.:**
   
   ```
   make add_events NUM_OF_EVENTS=10 NUM_OF_PARALLEL_PROCESS=1 ENV=tst2 BRAND=bma IS_LIVE=True IS_UPCOMING=False ADD_EXTENDED_MARKETS=False EVENT_PREFIX=MQA
   ```

**NOTE:**
   
      If it is required to create events with big number of markets value ADD_EXTENDED_MARKETS should be "True" in other case "False".

#### For starting *Live Updates Locust* in Terminal:

   ```
   locust -P 8088
   ```

#### For *Deleting events* run from Terminal:

   ```
   make delete_events ENV=some_env BRAND=some_brand FILE_WITH_EVENTS_IDS=some_file.json
   ```
   
   **E.g.:**
   
   
   ```
   make delete_events ENV=tst2 BRAND=bma FILE_WITH_EVENTS_IDS=file_with_events_ids_1575459888.366734.json
   ```
