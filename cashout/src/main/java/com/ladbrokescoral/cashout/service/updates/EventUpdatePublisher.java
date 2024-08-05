package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.config.InternalKafkaTopics;
import com.ladbrokescoral.cashout.model.response.EventDto;
import com.ladbrokescoral.cashout.model.response.UpdateEventResponse;
import java.math.BigInteger;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class EventUpdatePublisher {
  private final KafkaTemplate<String, Object> kafkaTemplate;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Autowired
  public EventUpdatePublisher(KafkaTemplate<String, Object> kafkaTemplate) {
    this.kafkaTemplate = kafkaTemplate;
  }

  public void eventUpdateRequest(String token, BigInteger eventId) {
    EventDto event = new EventDto(String.valueOf(eventId), true);
    UpdateEventResponse eventResponse = new UpdateEventResponse(event);
    ASYNC_LOGGER.info("EventUpdatePublisher :: eventUpdateRequest :: event :: {}", event);
    String topicName = InternalKafkaTopics.EVENT_UPDATES.getTopicName();
    kafkaTemplate.send(topicName, token, eventResponse);
  }
}
