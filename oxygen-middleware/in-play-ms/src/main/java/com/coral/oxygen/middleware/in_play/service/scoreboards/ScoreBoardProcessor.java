package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class ScoreBoardProcessor {

  private final EventValidator eventValidator;

  private final ScoreboardCache scoreboardCache;

  private final EventMapper eventMapper;

  public void processScoreBoardData(String eventId, String updatedMessage) {
    ScoreboardEvent newEvent = new ScoreboardEvent(eventId, updatedMessage);
    if (eventValidator.validate(newEvent)) {
      log.info("ScoreBoardProcessor:: it is a valid update for eventId::{}", eventId);
      Optional<ScoreboardEvent> previousEvent = scoreboardCache.findById(eventId);
      Optional<ScoreboardEvent> mappedNewEvent = eventMapper.sportMapper(newEvent);

      // publish updateMessage in string format to the Kafka or any
      // external
      // save to redis
      saveUpdateIfNewer(mappedNewEvent, previousEvent);
    } else {
      log.info(
          "Incoming update is not a valid update::{} for eventId::{}", updatedMessage, eventId);
    }
  }

  private void saveUpdateIfNewer(
      Optional<ScoreboardEvent> newEvent, Optional<ScoreboardEvent> previousEvent) {
    newEvent.ifPresent(
        (ScoreboardEvent event) -> {
          if (previousEvent.isEmpty() || event.isNewer(previousEvent.get())) {
            log.info("saving update {} for event {}", event.getSequenceId(), event.getObEventId());
            scoreboardCache.save(event);
          }
        });
  }
}
