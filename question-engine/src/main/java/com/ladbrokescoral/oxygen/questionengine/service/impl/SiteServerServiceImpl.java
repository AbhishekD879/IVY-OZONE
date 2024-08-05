package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.questionengine.service.SiteServerService;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@AllArgsConstructor
public class SiteServerServiceImpl implements SiteServerService {

  private static final String PERIOD_CODE = "periodCode";
  private static final String CHILDREN = "children";
  private static final String EVENT_FACT = "eventFact";
  private static final String FACT_CODE = "factCode";
  private static final String EVENT_PARTICIPANT_ID = "eventParticipantId";
  private static final String FACT = "fact";
  private static final String EVENT_PERIOD = "eventPeriod";
  private static final String ROLE_CODE = "roleCode";
  private static final String ID = "id";
  private static final String ALL = "ALL";
  private static final String SCORE = "SCORE";
  private static final String FINISH = "FINISH";
  
  private final SiteServerApi siteServerApi;
  
  public Optional<Event> getEventDetails(String eventId) {
    return siteServerApi.getCommentaryForEvent(Collections.singletonList(eventId))
        .map(List::stream)
        .orElse(Stream.empty())
        .findFirst();
  }

  public List<Integer> findScoresForEvent(Event event) {
    List<Children> commentaryData = event.getChildren();
    
    if (CollectionUtils.isNotEmpty(commentaryData)) {

      Map<String, EventParticipantRole> participantIdToRole = getParticipantIdToRole(commentaryData);
      Map<EventParticipantRole, Integer> roleToScore = getRoleToScore(commentaryData, participantIdToRole);

      if (roleToScore.get(EventParticipantRole.HOME) == null || roleToScore.get(EventParticipantRole.AWAY) == null) {
        return Collections.emptyList();
      }

      log.info("Found the following role to score: {}, Participant id to role: {}", roleToScore,  participantIdToRole);
      return Arrays.asList(roleToScore.get(EventParticipantRole.HOME), roleToScore.get(EventParticipantRole.AWAY));
    } else {
      return Collections.emptyList();
    }
  }

  private Map<String, EventParticipantRole> getParticipantIdToRole(List<Children> commentaryData) {
    return getEventParticipant(commentaryData)
        .collect(Collectors.toMap(
            eventParticipant -> (String) eventParticipant.get(ID),
            eventParticipant -> EventParticipantRole.valueOf((String) eventParticipant.get(ROLE_CODE))
        ));
  }

  private Stream<Map> getEventParticipant(List<Children> commentaryData) {
    return commentaryData.stream()
        .map(Children::getEventParticipant)
        .filter(Objects::nonNull);
  }

  private Map<EventParticipantRole, Integer> getRoleToScore(List<Children> commentaryData, Map<String, EventParticipantRole> participantIdToRole) {
    return getEventFacts(commentaryData)
        .filter(fact -> SCORE.equals(fact.get(FACT_CODE)))
        .map(fact -> new Object() {
          EventParticipantRole role = participantIdToRole.get(fact.get(EVENT_PARTICIPANT_ID).toString());
          int score = Integer.parseInt(fact.get(FACT).toString());
        })
        .collect(Collectors.toMap(scoreData -> scoreData.role, scoreData -> scoreData.score));
  }


  public boolean isMatchFinished(Event event) {
    boolean isEventResulted = event.getIsResulted() != null && event.getIsResulted();
    boolean hasMatchFinishedCommentary = 
        getEventPeriods(event)
        .anyMatch(eventPeriod -> FINISH.equals(eventPeriod.get(PERIOD_CODE)));

    return isEventResulted || hasMatchFinishedCommentary;
  }

  private Stream<Map<String, Object>> getEventFacts(List<Children> commentaryData) {
    return getFromAllEventPeriodsByKey(getAllPeriodCodes(commentaryData), EVENT_FACT);
  }
  
  private Stream<Map<String, Object>> getEventPeriods(Event event) {
    return getFromAllEventPeriodsByKey(getAllPeriodCodes(event.getChildren()), EVENT_PERIOD);
  }

  private Stream<List<Map<String, Object>>> getAllPeriodCodes(List<Children> commentaryData) {
    return commentaryData.stream()
        .map(Children::getEventPeriod)
        .filter(Objects::nonNull)
        .filter(eventPeriod -> ALL.equals(eventPeriod.get(PERIOD_CODE)))
        .map(eventPeriod -> eventPeriod.get(CHILDREN))
        .filter(Objects::nonNull)
        .map(this::cast);
  }
  
  private Stream<Map<String, Object>> getFromAllEventPeriodsByKey(Stream<List<Map<String, Object>>> allEventPeriods, String key) {
    return allEventPeriods
        .flatMap(List::stream)
        .map(eventPeriodData -> eventPeriodData.get(key))
        .filter(Objects::nonNull)
        .map(this::cast);
  }

  @SuppressWarnings("unchecked")
  private <T> T cast(Object obj) {
    return (T) obj;
  }

  private enum EventParticipantRole {
    HOME,
    AWAY
  }

}
