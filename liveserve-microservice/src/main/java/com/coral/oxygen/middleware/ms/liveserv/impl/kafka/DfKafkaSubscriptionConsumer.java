package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import com.coral.oxygen.middleware.ms.liveserv.impl.scoreboard.EventValidator;
import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class DfKafkaSubscriptionConsumer {

  private final KafkaInternalDFScoreboardsPublisher internalDFScoreboardsPublisher;
  private final EventValidator validator;

  public DfKafkaSubscriptionConsumer(
      KafkaInternalDFScoreboardsPublisher internalPublisher, EventValidator validator) {
    this.internalDFScoreboardsPublisher = internalPublisher;
    this.validator = validator;
  }

  @KafkaListener(
      topics = "${df.scoreboard.topic.name}",
      containerFactory = "filteredKafkaScoreBoardsContainerFactory")
  public void consume(
      @Header(name = "${scoreboard.topic.eventKey}") Optional<String> obEventId,
      ConsumerRecord<String, String> record) {
    obEventId.ifPresent(eventId -> validateAndPublish(eventId, record.value()));
  }

  private void validateAndPublish(String eventId, String updateMessage) {
    if (validator.validate(new ScoreboardEvent(eventId, updateMessage))) {
      internalDFScoreboardsPublisher.publish(eventId, updateMessage);
    }
  }
}
