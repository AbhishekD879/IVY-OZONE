package com.coral.oxygen.middleware.common.service

import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType
import spock.lang.Specification

class MarketTemplateNameServiceSpec extends Specification {

  MarketTemplateNameService marketTemplateNameService

  def setup() {
    marketTemplateNameService = new MarketTemplateNameService(
        ['Match Betting'] as String[],
        ['Match Result'] as String[],
        ['To Lift the trophy'] as String[],
        ['To finish 3rd'] as String[],
        ['To reach the final'] as String[],
        ['Next Team to Score'] as String[],
        ['Both Teams to Score'] as String[],
        [
          'Match Result and Both Teams To Score'
        ] as String[],
        ['Total Goals Over/Under'] as String[],
        ['To Qualify'] as String[],
        [
          'Penalty Shoot-Out Winner',
          'Penalty Shoot Out Winner'
        ] as String[],
        [
          'Extra-Time Result',
          'Extra Time Result'
        ] as String[],
        ['Draw No Bet'] as String[],
        ['First-Half Result'] as String[],
        ['Match Winner'] as String[],
        ['Money Line'] as String[],
        ['Fight Betting'] as String[],
        ['3 Ball Betting'] as String[],
        ['2 Ball Betting'] as String[],
        ['Handicap Match Result'] as String[],
        ['Handicap First Half'] as String[],
        [
          'Handicap Second Half',
          'Handi SC'
        ] as String[],
        ['Outright'] as String[],
        ['Win or Each Way'] as String[],
        Collections.emptyMap(),
        Collections.emptyMap(),
        ['Two up Market'] as String[],
        ['Each Way'] as String[],
        ['Total Points Over OR Under'] as String[])
    marketTemplateNameService.init()
  }

  def "test getting MarketTemplateType by name"() {
    expect:
    marketTemplateNameService.getType(name) == result

    where:
    name                       | result
    'Match Betting'            | MarketTemplateType.MATCH_BETTING
    'Match Result'             | MarketTemplateType.MATCH_RESULT
    'Next Team to Score'       | MarketTemplateType.NEXT_TEAM_TO_SCORE
    'Extra Time Result'        | MarketTemplateType.EXTRA_TIME_RESULT
    'Extra-Time Result'        | MarketTemplateType.EXTRA_TIME_RESULT
    'Penalty Shoot-Out Winner' | MarketTemplateType.PENALTY_SO_WINNER
    'Penalty Shoot Out Winner' | MarketTemplateType.PENALTY_SO_WINNER
  }

  def "test getting names by MarketTemplateType"() {
    expect:
    marketTemplateNameService.getNames(type) == result

    where:
    result                                                 | type
    ['Match Betting'] as String[]                          | MarketTemplateType.MATCH_BETTING
    ['Match Result'] as String[]                           | MarketTemplateType.MATCH_RESULT
    ['Next Team to Score'] as String[]                     | MarketTemplateType.NEXT_TEAM_TO_SCORE
    [
      'Extra-Time Result',
      'Extra Time Result'
    ] as String[] | MarketTemplateType.EXTRA_TIME_RESULT
    [
      'Handicap Second Half',
      'Handi SC',
      'Handicap First Half',
      'Handicap Match Result'
    ] as String[]                  | [
      MarketTemplateType.HANDICAP_SECOND_HALF,
      MarketTemplateType.HANDICAP_FIRST_HALF,
      MarketTemplateType.HANDICAP_MATCH_RESULT
    ]
  }

  def "test getting first market name by MarketTemplateType"() {
    expect:
    marketTemplateNameService.getFirstName(type) == result

    where:
    result                     | type
    'Match Betting'            | MarketTemplateType.MATCH_BETTING
    'Match Result'             | MarketTemplateType.MATCH_RESULT
    'Next Team to Score'       | MarketTemplateType.NEXT_TEAM_TO_SCORE
    'Extra-Time Result'        | MarketTemplateType.EXTRA_TIME_RESULT
    'Penalty Shoot-Out Winner' | MarketTemplateType.PENALTY_SO_WINNER
  }

  def "test contains market name in MarketTemplateType"() {
    expect:
    marketTemplateNameService.containsName(type, name) == result

    where:
    name                       | type                                  | result
    'Match Betting'            | MarketTemplateType.MATCH_BETTING      | true
    '|Match Betting|'          | MarketTemplateType.MATCH_BETTING      | true
    'Match Result'             | MarketTemplateType.MATCH_RESULT       | true
    'Match Results'            | MarketTemplateType.MATCH_RESULT       | false
    '|Match Results|'          | MarketTemplateType.MATCH_BETTING      | false
    'Next Team to Win'         | MarketTemplateType.NEXT_TEAM_TO_SCORE | false
    'Extra-Time Result'        | MarketTemplateType.EXTRA_TIME_RESULT  | true
    'Penalty Shoot-Out Winner' | MarketTemplateType.PENALTY_SO_WINNER  | true
    'Penalty ShootOut Winner'  | MarketTemplateType.PENALTY_SO_WINNER  | false
  }

  def "test get market template names as query by MarketTemplateType"() {
    expect:
    marketTemplateNameService.asQuery(types) == result

    where:

    types << [
      [],
      [
        MarketTemplateType.NEXT_TEAM_TO_SCORE
      ],
      [
        MarketTemplateType.MATCH_BETTING,
        MarketTemplateType.MATCH_RESULT
      ],
      [
        MarketTemplateType.EXTRA_TIME_RESULT,
        MarketTemplateType.PENALTY_SO_WINNER
      ]
    ]
    result << [
      '',
      '|Next Team to Score|,Next Team to Score',
      '|Match Betting|,|Match Result|,Match Betting,Match Result',
      '|Extra-Time Result|,|Extra Time Result|,|Penalty Shoot-Out Winner|,|Penalty Shoot Out Winner|,Extra-Time Result,Extra Time Result,Penalty Shoot-Out Winner,Penalty Shoot Out Winner'
    ]
  }
}
