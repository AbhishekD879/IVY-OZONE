package com.ladbrokescoral.oxygen.notification.services;

import com.ladbrokescoral.oxygen.notification.entities.Position;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.EventScores;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.utils.FootballCommentaryMapper;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class EventService {

  private static final String FOOTBALL_CATEGORY_ID = "16";
  private final SiteServerApiService siteServerApiService;
  private final Events events;

  @Autowired
  public EventService(final SiteServerApiService siteServerApiService, final Events events) {
    this.siteServerApiService = siteServerApiService;
    this.events = events;
  }

  public Optional<Event> getProcessedEvent(long eventId) {
    return events.findById(RedisKey.forEvent(eventId));
  }

  public Event process(long eventId) {
    return getProcessedEvent(eventId)
        .orElseGet(
            () -> {
              Event newEvent = consumeEvent(String.valueOf(eventId));
              events.save(newEvent.setId(RedisKey.forEvent(eventId)));
              return newEvent;
            });
  }

  public List<Position> getResultsForEvent(long eventId) {
    return siteServerApiService
        .getCachedRacingResults(String.valueOf(eventId))
        .map(ObjectMapper::toPositions)
        .orElse(Collections.emptyList());
  }

  public Event getEventForOutcome(String outcomeId) {
    return siteServerApiService
        .getCachedEventForOutcome(outcomeId)
        .map(ObjectMapper::toEvent)
        .orElse(null);
  }

  private Event consumeEvent(String eventId) {
    return siteServerApiService
        .getEvent(String.valueOf(eventId))
        .map(this::mapToEvent)
        .orElseThrow(
            () ->
                new ConsumeEventException(
                    String.format("Can't load initial data for event id: %s", eventId)));
  }

  private Event mapToEvent(com.egalacoral.spark.siteserver.model.Event event) {
    if (isFootballEvent(event)) {
      Optional<EventScores> eventScores = getEventScoresFromCommentary(event.getId());
      if (eventScores.isPresent()) {
        return ObjectMapper.toEventWithScores(event, eventScores.get());
      }
    }
    return ObjectMapper.toEvent(event);
  }

  private Optional<EventScores> getEventScoresFromCommentary(String eventId) {
    return siteServerApiService
        .getCommentaryForEvent(eventId)
        .map(FootballCommentaryMapper::toEventScores)
        .filter(c -> !CollectionUtils.isEmpty(c.getTeams()) && c.getTeams().size() == 2);
  }

  private boolean isFootballEvent(com.egalacoral.spark.siteserver.model.Event event) {
    return Objects.nonNull(event) && event.getCategoryId().equals(FOOTBALL_CATEGORY_ID);
  }
}
