package com.coral.oxygen.edp.model.mapping.converter

import com.coral.oxygen.edp.model.output.OutputMarket
import spock.lang.Specification
import spock.lang.Unroll

import static com.coral.oxygen.edp.TestUtil.*

class MarketGroupAndSortConverterSpec extends Specification {

  MarketGroupAndSortConverter marketGroupAndSortConverter

  def setup() {
    marketGroupAndSortConverter = new MarketGroupAndSortConverter()
  }

  @Unroll
  def "Markets with marketTemplateName '#marketTemplate' should be in the #groupPositionName group"() {
    expect:
    def inputMarkets = deserializeListWithJackson("/marketGroupAndSortConverter/" + testFileJson, OutputMarket.class)
    Collection<List<OutputMarket>> result = marketGroupAndSortConverter.convert(inputMarkets)

    result.size() == 2
    List<OutputMarket> group = result.asList().get(index)
    group.size() != 1

    group.get(0).id == "12"
    group.get(1).id == "11"


    where:
    marketTemplate                               | testFileJson             | groupPositionName  | index
    "Match Result and Over/Under X Goals"        | "mraougFirst.json"       | "first"            | 0
    "Match Result and Over/Under X Goals"        | "mraougSecond.json"      | "second"           | 1
    "Both Teams to Score and Over/Under X Goals" | "bttsaougFirst.json"     | "first"            | 0
    "Both Teams to Score and Over/Under X Goals" | "bttsaougSecond.json"    | "second"           | 1
    "Team Specials"                              | "tsFirst.json"           | "first"            | 0
    "Team Specials"                              | "tsSecond.json"          | "second"           | 1
    "Player Specials (O/U)"                      | "psSecond.json"          | "second"           | 1
    "Player Specials (O/U)"                      | "psFirst.json"           | "first"            | 0
    "Match Specials"                             | "msFirst.json"           | "first"            | 0
    "Match Specials"                             | "msSecond.json"          | "second"           | 1
    "InPlay Specials"                            | "isSecond.json"          | "second"           | 1
    "InPlay Specials"                            | "isFirst.json"           | "first"            | 0
    "YourCall"                                   | "ycFirst.json"           | "first"            | 0
    "YourCall"                                   | "ycSecond.json"          | "second"           | 1
    "First Half and Over/Under X Goals"          | "fhaougFirst.json"       | "first"            | 0
    "First Half and Over/Under X Goals"          | "fhaougSecond.json"      | "second"           | 1
    "Second Half and Over/Under X Goals"         | "shaougSecond.json"      | "second"           | 1
    "Second Half and Over/Under X Goals"         | "shaougFirst.json"       | "first"            | 0
    "Handicap Match Result X - X"                | "hmr.json"               | "first"            | 0
    "Handicap First Half X - X"                  | "hfh.json"               | "first"            | 0
    "Handicap Second Half X - X"                 | "hsh.json"               | "first"            | 0
    "Over/Under Total Goals X"                   | "outg.json"              | "first"            | 0
    "Over/Under First Half X"                    | "oufh.json"              | "first"            | 0
    "Over/Under Second Half X"                   | "oush.json"              | "first"            | 0
    "Over/Under <home_team> Total Goals X"       | "ouHomeTeam.json"        | "first"            | 0
    "Over/Under <away_team> Total Goals X"       | "ouAwayTeam.json"        | "first"            | 0
    "Over/Under <home/away>team Total Goals X"   | "ouHomeAwayTeam.json"    | "first"            | 0
    "Over/Under First Half <home_team> X"        | "oufhHomeTeam.json"      | "first"            | 0
    "Over/Under First Half <home/away>team X"    | "oufhHomeAwayTeam.json"  | "first"            | 0
    "Over/Under Second Half <home_team> X"       | "oushHomeTeam.json"      | "first"            | 0
    "Over/Under Second Half <home/away>team X"   | "oushHomeAwayTeam.json"  | "first"            | 0
  }

  def "Markets with the same marketTemplateName should be grouped"() {
    given:
    def inputMarkets = deserializeListWithJackson("/marketGroupAndSortConverter/allGroups.json", OutputMarket.class)

    when:
    Collection<List<OutputMarket>> result = marketGroupAndSortConverter.convert(inputMarkets)

    then: "result should contain 9 groups with markets that matched regex and 1 group with markets " +
    "that have the same marketTemplateName ('Match Betting' marketTemplateName)"
    result.size() == 10
  }
}
