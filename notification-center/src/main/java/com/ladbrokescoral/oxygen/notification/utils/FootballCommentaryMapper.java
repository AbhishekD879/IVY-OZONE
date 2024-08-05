package com.ladbrokescoral.oxygen.notification.utils;

import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.EventScores;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class FootballCommentaryMapper {

  private static final String PENALTIES_PERIOD = "PENALTIES";

  public static EventScores toEventScores(Event commentaryEvent) {
    String lastPeriod = null;

    Map<String, EventScores.Team> participants = initTeams(commentaryEvent);
    Map eventPeriod = getEventPeriod(commentaryEvent);
    List<Map<String, Object>> subPeriods = extractSubPeriodsOrderedByStartTimeDesc(eventPeriod);

    if (subPeriods.isEmpty()) {
      Map<String, Integer> factScores = extractFactScores(eventPeriod);
      factScores.forEach(
          (participant, score) ->
              participants.getOrDefault(participant, new EventScores.Team()).setScore(score));
    } else {
      lastPeriod = (String) subPeriods.get(0).get(EventPeriodField.PERIOD_CODE);

      subPeriods.forEach(
          p -> {
            String period = String.valueOf(p.get(EventPeriodField.PERIOD_CODE));
            Map<String, Integer> factScores = extractFactScores(p);
            factScores.forEach(
                (participant, score) ->
                    updateTeamWithScore(
                        participants.getOrDefault(participant, new EventScores.Team()),
                        period,
                        score));
          });
    }

    return new EventScores(lastPeriod, new ArrayList<>(participants.values()));
  }

  private static void updateTeamWithScore(EventScores.Team team, String period, Integer score) {
    if (PENALTIES_PERIOD.equals(period)) {
      team.setPenalties(score);
    } else {
      team.setScore(team.getScore() + score);
    }
  }

  private static Map<String, Integer> extractFactScores(Map eventPeriod) {
    return getChildrenStream(eventPeriod, EventPeriodField.EVENT_FACT)
        .filter(
            factMap ->
                factMap.containsKey(EventFactField.FACT_CODE)
                    && factMap.get(EventFactField.FACT_CODE).equals(EventFactField.FACT_CODE_SCORE))
        .collect(
            Collectors.toMap(
                factMap -> String.valueOf(factMap.get(EventFactField.EVENT_PARTICIPANT_ID)),
                factMap -> Integer.valueOf(String.valueOf(factMap.get(EventFactField.FACT)))));
  }

  private static Map getEventPeriod(Event commentaryEvent) {
    return commentaryEvent.getConcreteChildren(Children::getEventPeriod).stream()
        .findAny()
        .orElse(Collections.emptyMap());
  }

  private static Map<String, EventScores.Team> initTeams(Event commentaryEvent) {
    return commentaryEvent.getConcreteChildren(Children::getEventParticipant).stream()
        .collect(
            Collectors.toMap(
                p -> String.valueOf(p.get(EventParticipantField.ID)),
                p ->
                    new EventScores.Team(
                        String.valueOf(p.get(EventParticipantField.NAME)),
                        String.valueOf(p.get(EventParticipantField.ROLE_CODE)))));
  }

  private static List<Map<String, Object>> extractSubPeriodsOrderedByStartTimeDesc(
      Map eventPeriod) {
    return getChildrenStream(eventPeriod, EventPeriodField.EVENT_PERIOD)
        .sorted(
            Comparator.comparing(
                    (Map<String, Object> period) ->
                        String.valueOf(period.get(EventPeriodField.START_TIME)))
                .reversed())
        .collect(Collectors.toList());
  }

  private static Stream<Map<String, Object>> getChildrenStream(Map eventPeriod, String childName) {
    return ((List<Map<String, Object>>)
            eventPeriod.getOrDefault(EventPeriodField.CHILDREN, Collections.emptyList()))
        .stream()
            .filter(Objects::nonNull)
            .filter(table -> table.containsKey(childName))
            .map(table -> (Map<String, Object>) table.get(childName));
  }

  private static class EventPeriodField {
    private static final String START_TIME = "startTime";
    private static final String CHILDREN = "children";
    private static final String PERIOD_CODE = "periodCode";
    private static final String EVENT_FACT = "eventFact";
    private static final String EVENT_PERIOD = "eventPeriod";
  }

  private static class EventParticipantField {
    private static final String ID = "id";
    private static final String NAME = "name";
    private static final String ROLE_CODE = "roleCode";
  }

  private static class EventFactField {
    private static final String FACT_CODE = "factCode";
    private static final String FACT = "fact";
    private static final String EVENT_PARTICIPANT_ID = "eventParticipantId";
    private static final String FACT_CODE_SCORE = "SCORE";
  }
}
