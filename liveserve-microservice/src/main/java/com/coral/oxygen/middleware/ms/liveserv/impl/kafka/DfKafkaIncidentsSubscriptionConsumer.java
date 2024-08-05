package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncidentsValidator;
import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class DfKafkaIncidentsSubscriptionConsumer {

  private final KafkaIncidentsPublisher kafkaIncidentsPublisher;
  private final IncidentsValidator validator;
  private static final String SPORT_CATEGORY = "SOCCER";

  public DfKafkaIncidentsSubscriptionConsumer(
      KafkaIncidentsPublisher kafkaIncidentsPublisher, IncidentsValidator validator) {
    this.kafkaIncidentsPublisher = kafkaIncidentsPublisher;
    this.validator = validator;
  }

  /**
   * This Method is used to Consume Incidents Message which is coming from Feed
   *
   * @param obEventId
   * @param sportCategory
   * @param incidentsMesssage
   */
  @KafkaListener(
      topics = "${df.incidents.topic.name}",
      containerFactory = "filteredKafkaScoreBoardsContainerFactory")
  public void consume(
      @Header(name = "${df.incidents.topic.eventKey}") Optional<String> obEventId,
      @Header(name = "${incident.sport.category}") String sportCategory,
      ConsumerRecord<String, String> incidentsMesssage) {
    log.info(
        "consume EventId {} sportCateogry {} incidentsMesssage {} ",
        obEventId,
        sportCategory,
        incidentsMesssage.value());
    if (obEventId.isPresent() && SPORT_CATEGORY.equalsIgnoreCase(sportCategory)) {
      validateAndPublish(obEventId.get(), incidentsMesssage.value());
    } else {
      log.info("This sport category was not processed for incidents data {}", sportCategory);
    }
  }

  /**
   * This Method is used to filter Feed ,VAR & Match Fact Codes and publish into Internal Kafka
   *
   * @param eventId
   * @param updateMessage
   */
  private void validateAndPublish(String eventId, String updateMessage) {
    log.info(
        "incidents validatoin {}", validator.validate(new IncidentsEvent(eventId, updateMessage)));
    if (validator.validate(new IncidentsEvent(eventId, updateMessage))) {
      kafkaIncidentsPublisher.publish(eventId, updateMessage);
    }
  }
}
