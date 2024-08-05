package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import com.coral.oxygen.middleware.ms.liveserv.impl.redis.ScoreboardCache;
import com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard.EventMapper;
import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Optional;
import javax.json.Json;
import javax.json.JsonObject;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class InternalDfKafkaConsumer {

  private final ScoreboardCache scoreboardCache;
  private final KafkaScoreboardsPublisher scoreboardsPublisher;
  private final EventMapper mapper;

  @Autowired
  public InternalDfKafkaConsumer(
      ScoreboardCache scoreboardCache, KafkaScoreboardsPublisher publisher) {
    this.scoreboardCache = scoreboardCache;
    this.scoreboardsPublisher = publisher;
    mapper = new EventMapper();
  }

  @KafkaListener(
      topics = "${topic.internal.df.scoreboards}",
      containerFactory = "internalDFKafkaFactory")
  public void consume(ConsumerRecord<String, String> record) {
    ScoreboardEvent newEvent = new ScoreboardEvent(record.key(), record.value());
    Optional<ScoreboardEvent> previousEvent = scoreboardCache.findById(record.key());
    Optional<ScoreboardEvent> mappedNewEvent = mapper.sportMapper(newEvent);
    getIncrementalUpdate(newEvent, mappedNewEvent, previousEvent)
        .ifPresent(update -> publishUpdate(newEvent.getObEventId(), update));

    saveUpdateIfNewer(mappedNewEvent, previousEvent);
  }

  private Optional<String> getIncrementalUpdate(
      ScoreboardEvent newEvent,
      Optional<ScoreboardEvent> mappedNewEvent,
      Optional<ScoreboardEvent> previousEvent) {
    if (!previousEvent.isPresent()) {
      return mappedNewEvent.map(ScoreboardEvent::getEventStructure).map(JsonObject::toString);
    }

    return previousEvent
        .filter(newEvent::isNewer)
        .map(prev -> getJsonDiff(mappedNewEvent.orElse(newEvent), prev));
  }

  private void publishUpdate(String obEventId, String update) {
    scoreboardsPublisher.publish(obEventId, update);
    log.info("Published {} scoreboard update {}", obEventId, update);
  }

  private String getJsonDiff(ScoreboardEvent newEvent, ScoreboardEvent previous) {
    JsonObject jsonDiff =
        Json.createMergeDiff(previous.getRawStructure(), newEvent.getRawStructure())
            .toJsonValue()
            .asJsonObject();

    return mapper.mapToUpdateStructure(jsonDiff, newEvent.getObEventId());
  }

  private void saveUpdateIfNewer(
      Optional<ScoreboardEvent> newEvent, Optional<ScoreboardEvent> previousEvent) {
    newEvent.ifPresent(
        (ScoreboardEvent event) -> {
          if (!previousEvent.isPresent() || event.isNewer(previousEvent.get())) {
            log.debug("saving update {} for event {}", event.getSequenceId(), event.getObEventId());
            scoreboardCache.save(event);
          }
        });
  }
}
