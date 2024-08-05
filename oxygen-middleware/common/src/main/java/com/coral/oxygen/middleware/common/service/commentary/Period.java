package com.coral.oxygen.middleware.common.service.commentary;

import com.google.common.collect.Sets;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import org.apache.commons.lang3.math.NumberUtils;

public class Period extends AbstractModel {

  private static final FactScore[] EMPTY_FACT_SCORES = new FactScore[0];

  private static final String PENALTIES_PERIOD = "PENALTIES";
  private static final Set<String> MAIN_PERIODS = Sets.newHashSet("SECOND_HALF", "FIRST_HALF");
  private static final Set<String> EXTRA_PERIODS =
      Sets.newHashSet("EXTRA_TIME_SECOND_HALF", "EXTRA_TIME_FIRST_HALF");
  private static final Set<String> PROCESSED_PERIODS = new HashSet<>();

  static {
    PROCESSED_PERIODS.add(PENALTIES_PERIOD);
    PROCESSED_PERIODS.addAll(MAIN_PERIODS);
    PROCESSED_PERIODS.addAll(EXTRA_PERIODS);
  }

  public enum FieldNames {
    id,
    eventId,
    periodCode,
    description,
    startTime,
    children,
    subPeriods,
    teamScores,
    periodIndex
  }

  private class ChildKey {
    static final String EVENT_PERIOD = "eventPeriod";
    static final String EVENT_FACT = "eventFact";
    static final String EVENT_INCIDENT = "eventIncident";
  }

  public Period(Map<String, Object> fields) {
    super(fields);
  }

  public FactScore[] extractScores(String homeId) {
    if (getChildren() == null) {
      return EMPTY_FACT_SCORES;
    }
    FactScore[] scores = new FactScore[2];
    List<FactScore> scoresList = getScoreFacts();
    if (scoresList.isEmpty() || scoresList.size() != 2) {
      return EMPTY_FACT_SCORES;
    }
    if (scoresList.get(0).getField(FactScore.FieldNames.eventParticipantId).equals(homeId)) {
      scores[0] = scoresList.get(0);
      scores[1] = scoresList.get(1);
    } else {
      scores[1] = scoresList.get(0);
      scores[0] = scoresList.get(1);
    }
    return scores;
  }

  public List<Period> extractSubPeriods() {
    return this.getChildren().stream()
        .filter(Objects::nonNull)
        .filter(table -> table.containsKey(ChildKey.EVENT_PERIOD))
        .filter(
            table -> {
              Map<String, Object> test = (Map<String, Object>) table.get(ChildKey.EVENT_PERIOD);
              return Period.PROCESSED_PERIODS.contains(
                  test.get(Period.FieldNames.periodCode.toString()).toString());
            })
        .map(table -> new Period((Map<String, Object>) table.get(ChildKey.EVENT_PERIOD)))
        .collect(Collectors.toList());
  }

  public List<FactScore> getScoreFacts() {
    return getChildren().stream()
        .filter(table -> table.containsKey(ChildKey.EVENT_FACT))
        .map(table -> (Map<String, Object>) table.get(ChildKey.EVENT_FACT))
        .filter(FactScore::isFactScore)
        .map(FactScore::new)
        .collect(Collectors.toList());
  }

  public List<Period> getGamePeriods() {
    return getChildren().stream()
        .filter(table -> table.containsKey(ChildKey.EVENT_PERIOD))
        .map(table -> (Map<String, Object>) table.get(ChildKey.EVENT_PERIOD))
        .map(Period::new)
        .filter(Period::isGame)
        .collect(Collectors.toList());
  }

  public static List<Period> listFromFacts(List<Object> facts) {
    return facts.stream()
        .filter(f -> f instanceof Map)
        .map(Map.class::cast)
        .map(f -> f.get(ChildKey.EVENT_PERIOD))
        .filter(Objects::nonNull)
        .map(eventPeriod -> new Period((Map<String, Object>) eventPeriod))
        .collect(Collectors.toList());
  }

  public List<Map<String, Object>> getChildren() {
    return (List<Map<String, Object>>) getField(FieldNames.children);
  }

  public String getPeriodCode() {
    return getField(FieldNames.periodCode).toString();
  }

  public boolean isGame() {
    return "GAME".equals(getField(FieldNames.periodCode));
  }

  public boolean isSet() {
    return "SET".equals(getField(FieldNames.periodCode));
  }

  public boolean isPenaltiesPeriod() {
    return PENALTIES_PERIOD.equals(getPeriodCode());
  }

  public boolean isMainPeriod() {
    return MAIN_PERIODS.contains(getPeriodCode());
  }

  public boolean isExtraPeriod() {
    return EXTRA_PERIODS.contains(getPeriodCode());
  }

  public Integer getPeriodIndex() {
    String indexStr = getField(FieldNames.periodIndex).toString();
    return NumberUtils.isDigits(indexStr) ? Integer.parseInt(indexStr) : null;
  }
}
