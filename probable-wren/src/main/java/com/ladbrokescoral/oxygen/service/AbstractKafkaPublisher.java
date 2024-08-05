package com.ladbrokescoral.oxygen.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Slf4j
@RequiredArgsConstructor
public class AbstractKafkaPublisher {

  private final KafkaTemplate<String, String> kafkaTemplate;
  private final String topic;

  public void publish(String key, String message) {
    log.info("[Kafka] topic: {} key: {} message: {}", topic, key, message);
    kafkaTemplate
        .send(topic, key, message)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, String>>() {

              @Override
              public void onSuccess(final SendResult<String, String> message) {
                log.debug(
                    "[Kafka] sent message= {}} with offset= {}",
                    message,
                    message.getRecordMetadata().offset());
              }

              @Override
              public void onFailure(final Throwable throwable) {
                log.error("Unable to send message to topic = " + topic, throwable);
              }
            });
  }
}
