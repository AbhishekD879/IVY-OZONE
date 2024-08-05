package com.coral.oxygen.middleware.pojos.model.output;

import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.*;

import java.util.Arrays;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;

public enum PrimaryMarkets {
  // The order of primary markets from left to right.
  // all sports with -1 ID didn't verify in back-office.
  FOOTBALL(
      "FOOTBALL",
      16,
      MATCH_BETTING,
      MATCH_RESULT,
      EXTRA_TIME_RESULT,
      PENALTY_SO_WINNER,
      TO_QUALIFY,
      TO_LIFT_THE_TROPHY,
      TO_FINISH_THIRD,
      TO_REACH_THE_FINAL),

  BASKETBALL("BASKETBALL", 6, MONEY_LINE, MATCH_BETTING, MATCH_RESULT),

  TENNIS("TENNIS", 34, MATCH_BETTING),

  RUGBY_UNION("RUGBY_UNION", 31, MATCH_BETTING),

  RUGBY_LEAGUE("RUGBY_LEAGUE", 30, MATCH_BETTING),

  AMERICAN_FB("AMERICAN_FB", 1, MONEY_LINE, MATCH_BETTING, MATCH_RESULT),

  NON_FOOTBALL(
      "Other than Football",
      -1,
      MATCH_BETTING,
      MATCH_WINNER,
      MONEY_LINE,
      FIGHT_BETTING,
      THREE_BALL_BETTING,
      TWO_BALL_BETTING),

  VIRTUAL_EVENTS(
      "VIRTUAL",
      39,
      WIN_OR_EACH_WAY,
      MATCH_BETTING,
      MATCH_WINNER,
      TOTAL_GOALS_OVER_UNDER,
      EACH_WAY,
      TOTAL_POINTS_OVER_UNDER),

  HORSE_RACING("HORSE_RACING", 21, WIN_OR_EACH_WAY);

  /**
   * Primary markets per each sport: UFC("UFC", -1, "|Fight Betting|"), BOXING("BOXING", -1, "|Fight
   * Betting|"), BASEBALL("BASEBALL", -1, "|Money Line|", "|Match Betting|", "|Match Result|"),
   * BASKETBALL("BASKETBALL", 6, "|Money Line|", "|60 Minutes Betting|", "|Match Betting|", "|Match
   * Result|"), AMERICAN_FOOTBALL("AMERICAN_FB", 1, "|Money Line|", "|60 Minutes Betting|", "|Match
   * Betting|", "|Match Result|"), ICE_HOCKEY("ICE HOCKEY", 22, "|Money Line|", "|60 Minutes
   * Betting|", "|Match Result|"), HANDBALL("HANDBALL", -1, "|Match Betting|", "|Match Result|",
   * "|60 Minutes Betting|"), AUSSIE_RULES("AUSTRALIAN_RULES", 9, "|Match Betting|", "|Money
   * Line|"), BEACH_VOLLEYBALL("BEACH_VOLLEYBALL", -1, "|Match Betting|", "|Match Betting
   * Head/Head|"), DARTS("DARTS", -1, "|Match Betting|"), SNOOKER("SNOOKER", -1, "|Match Betting|"),
   * TABLE_TENNIS("TABLE TENNIS", 335, "|Match Betting|", "|Match Betting Head/Head|"),
   * TENNIS("TENNIS", -1, "|Match Betting|"), VOLLEYBALL("VOLLEYBALL", -1, "|Match Betting|",
   * "|Match Result|"), FUTSAL("FUTSAL", -1, "|Match Betting|"), GAELIC_FOOTBALL("GAELIC_FOOTBALL",
   * -1, "|Match Betting|"), RUGBY_LEAGUE("RUGBY_LEAGUE", -1, "|Match Betting|"),
   * RUGBY_UNION("RUGBY_UNION", -1, "|Match Betting|"), CRICKET("CRICKET", -1, "|Match Betting|",
   * "|Match Betting Head/Head|"), GOLF("GOLF", -1, "|1st Round 2 Ball Betting|", "|2nd Round 2 Ball
   * Betting|", "|3rd Round 2 Ball Betting|", "|4th Round" + " 2" + " Ball Betting|", "|1st Round 3
   * Ball " + "Betting|", "|2nd Round 3 Ball Betting|", "|3rd Round 3 Ball Betting|", "|4th Round 3
   * Ball Betting|", "|1st Round 2 Ball|", "|2nd Round 2 Ball|", "|3rd Round 2 Ball|", "|4th Round 2
   * Ball|", "|1st Round 3 Ball|", "|2nd Round 3 Ball|", "|3rd Round 3 Ball|", "|4th Round 3
   * Ball|"), HURLING("HURLING", -1, "|Match Betting|")
   */
  private String sport;

  private int sportId;
  private List<MarketTemplateType> primaryMarketTypes;

  PrimaryMarkets(String sport, int sportId, MarketTemplateType... primaryMarketTypes) {
    this.sport = sport;
    this.sportId = sportId;
    this.primaryMarketTypes = Arrays.asList(primaryMarketTypes);
  }

  public int getOrderIndex(MarketTemplateType marketType) {
    int i = primaryMarketTypes.indexOf(marketType);
    return i == -1 ? Integer.MAX_VALUE : i;
  }

  public int getSportId() {
    return sportId;
  }

  public String getSport() {
    return sport;
  }

  public Set<MarketTemplateType> getPrimaryMarkets() {
    return EnumSet.copyOf(primaryMarketTypes);
  }

  public static PrimaryMarkets enumerize(String name) {
    if (name == null) {
      return null;
    }
    for (PrimaryMarkets eventToMarket : values()) {
      if (eventToMarket.name().equalsIgnoreCase(name)
          || eventToMarket.getSport().equalsIgnoreCase(name)) {
        return eventToMarket;
      }
    }
    return null;
  }
}
