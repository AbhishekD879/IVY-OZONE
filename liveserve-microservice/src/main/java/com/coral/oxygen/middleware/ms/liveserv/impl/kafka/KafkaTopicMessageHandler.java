package com.coral.oxygen.middleware.ms.liveserv.impl.kafka;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EventMessageEnvelope;
import com.google.gson.Gson;
import com.newrelic.api.agent.NewRelic;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class KafkaTopicMessageHandler implements MessageHandler {

  private static final String CUSTOM_PUBLISH_UPDATE_COUNTER = "Custom/publishUpdate";
  private final Gson gson;
  private final KafkaUpdatePublisher kafkaPublisher;

  @Autowired
  public KafkaTopicMessageHandler(Gson gson, KafkaUpdatePublisher kafkaPublisher) {
    this.gson = gson;
    this.kafkaPublisher = kafkaPublisher;
  }

  @Override
  public void handle(EventMessageEnvelope envelope) {
    String channel = envelope.getChannel();
    String json = gson.toJson(envelope);

    log.trace("Publish channel update '{}' - {}", channel, json);
    NewRelic.incrementCounter(CUSTOM_PUBLISH_UPDATE_COUNTER);
    kafkaPublisher.publish(String.valueOf(envelope.getEventId()), json);
  }
}
