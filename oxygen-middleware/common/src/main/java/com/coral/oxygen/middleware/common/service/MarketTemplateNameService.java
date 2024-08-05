package com.coral.oxygen.middleware.common.service;

import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.*;

import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.annotation.PostConstruct;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Component
@NoArgsConstructor
@AllArgsConstructor
public class MarketTemplateNameService {

  @Value("${market.template.matchBetting}")
  private String[] matchBettingName;

  @Value("${market.template.matchResult}")
  private String[] matchResultName;

  @Value("${market.template.toLiftTrophy}")
  private String[] toLiftTrophyName;

  @Value("${market.template.toFinishThird}")
  private String[] toFinishThirdName;

  @Value("${market.template.toReachFinal}")
  private String[] toReachFinalName;

  @Value("${market.template.nextTeamToScore}")
  private String[] nextTeamToScoreName;

  @Value("${market.template.bothTeamToScore}")
  private String[] bothTeamToScoreName;

  @Value("${market.template.matchResultAndBothTeamToScore}")
  private String[] matchResultAndBothTeamToScore;

  @Value("${market.template.totalGoalsOverUnder}")
  private String[] totalGoalsOverUnderName;

  @Value("${market.template.toQualify}")
  private String[] toQualifyName;

  @Value("${market.template.penaltyShootOutWinner}")
  private String[] penaltyShootOutWinnerName;

  @Value("${market.template.extraTime}")
  private String[] extraTimeName;

  @Value("${market.template.drawNoBet}")
  private String[] drawNoBetName;

  @Value("${market.template.firstHalfResult}")
  private String[] firstHalfResultName;

  @Value("${market.template.matchWinner}")
  private String[] matchWinnerName;

  @Value("${market.template.moneyLine}")
  private String[] moneyLineName;

  @Value("${market.template.fightBetting}")
  private String[] fightBettingName;

  @Value("${market.template.threeBallBetting}")
  private String[] threeBallBettingName;

  @Value("${market.template.twoBallBetting}")
  private String[] twoBallBettingName;

  @Value("${market.template.handicapMatchResult}")
  private String[] handicapMatchResultName;

  @Value("${market.template.handicapFirstHalf}")
  private String[] handicapFirstHalfName;

  @Value("${market.template.handicapSecondHalf}")
  private String[] handicapSecondHalfName;

  @Value("${market.template.outright}")
  private String[] outrightName;

  @Value("${market.template.winOrEachWay}")
  private String[] winOrEachWayName;

  private Map<MarketTemplateType, String[]> marketTemplatesMap;
  private Map<String, MarketTemplateType> marketNameToTypeMap;

  @Value("${market.template.twoUpResult}")
  private String[] twoUpResult;

  @Value("${market.template.eachWay}")
  private String[] eachWay;

  @Value("${market.template.totalPointsOverAndUnder}")
  private String[] totalPointsOverAndUnder;

  @PostConstruct
  public void init() {
    marketTemplatesMap = new EnumMap<>(MarketTemplateType.class);
    marketTemplatesMap.put(MATCH_BETTING, matchBettingName);
    marketTemplatesMap.put(MATCH_RESULT, matchResultName);
    marketTemplatesMap.put(TO_LIFT_THE_TROPHY, toLiftTrophyName);
    marketTemplatesMap.put(TO_FINISH_THIRD, toFinishThirdName);
    marketTemplatesMap.put(TO_REACH_THE_FINAL, toReachFinalName);
    marketTemplatesMap.put(NEXT_TEAM_TO_SCORE, nextTeamToScoreName);
    marketTemplatesMap.put(BOTH_TEAMS_TO_SCORE, bothTeamToScoreName);
    marketTemplatesMap.put(MATCH_RESULT_AND_BOTH_TEAMS_TO_SCORE, matchResultAndBothTeamToScore);
    marketTemplatesMap.put(TOTAL_GOALS_OVER_UNDER, totalGoalsOverUnderName);
    marketTemplatesMap.put(TO_QUALIFY, toQualifyName);
    marketTemplatesMap.put(PENALTY_SO_WINNER, penaltyShootOutWinnerName);
    marketTemplatesMap.put(EXTRA_TIME_RESULT, extraTimeName);
    marketTemplatesMap.put(DRAW_NO_BET, drawNoBetName);
    marketTemplatesMap.put(FIRST_HALF_RESULT, firstHalfResultName);
    marketTemplatesMap.put(MATCH_WINNER, matchWinnerName);
    marketTemplatesMap.put(MONEY_LINE, moneyLineName);
    marketTemplatesMap.put(FIGHT_BETTING, fightBettingName);
    marketTemplatesMap.put(THREE_BALL_BETTING, threeBallBettingName);
    marketTemplatesMap.put(TWO_BALL_BETTING, twoBallBettingName);
    marketTemplatesMap.put(HANDICAP_MATCH_RESULT, handicapMatchResultName);
    marketTemplatesMap.put(HANDICAP_FIRST_HALF, handicapFirstHalfName);
    marketTemplatesMap.put(HANDICAP_SECOND_HALF, handicapSecondHalfName);
    marketTemplatesMap.put(OUTRIGHT, outrightName);
    marketTemplatesMap.put(WIN_OR_EACH_WAY, winOrEachWayName);
    marketTemplatesMap.put(TWO_UP_RESULT, twoUpResult);
    marketTemplatesMap.put(EACH_WAY, eachWay);
    marketTemplatesMap.put(TOTAL_POINTS_OVER_UNDER, totalPointsOverAndUnder);
    marketNameToTypeMap = new HashMap<>();
    marketTemplatesMap.forEach(
        (type, names) -> {
          for (String name : names) {
            marketNameToTypeMap.put(name.toLowerCase(), type);
          }
        });
  }

  public MarketTemplateType getType(String name) {
    name = ObjectUtils.isEmpty(name) ? name : name.toLowerCase();
    return marketNameToTypeMap.get(name);
  }

  public String[] getNames(MarketTemplateType marketTemplateType) {
    return marketTemplatesMap.get(marketTemplateType);
  }

  public String[] getNames(Collection<MarketTemplateType> markets) {
    return markets.stream().flatMap(m -> Stream.of(getNames(m))).toArray(String[]::new);
  }

  public String getFirstName(MarketTemplateType market) {
    return getNames(market)[0];
  }

  public boolean containsName(MarketTemplateType marketType, String templateMarketName) {
    String withoutPipes = templateMarketName.replaceAll("\\|", "");
    return Stream.of(getNames(marketType)).anyMatch(market -> market.contains(withoutPipes));
  }

  public String asQuery(Collection<MarketTemplateType> primaryMarkets) {
    return Stream.concat(
            primaryMarkets.stream().flatMap(m -> Stream.of(getNames(m))).map(n -> "|" + n + "|"),
            primaryMarkets.stream().flatMap(m -> Stream.of(getNames(m))))
        .collect(Collectors.joining(","));
  }

  public String asQueryFromMarketStrings(String[] primaryMarkets) {
    return Arrays.stream(primaryMarkets)
        .map(n -> "|" + n + "|," + n)
        .collect(Collectors.joining(","));
  }

  public String asQuery(MarketTemplateType templateType) {
    return asQuery(Collections.singleton(templateType));
  }
}
