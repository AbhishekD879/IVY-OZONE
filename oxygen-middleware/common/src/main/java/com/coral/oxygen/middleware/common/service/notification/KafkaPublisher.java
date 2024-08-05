package com.coral.oxygen.middleware.common.service.notification;

import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Slf4j
@RequiredArgsConstructor
public class KafkaPublisher implements MessagePublisher {

  private final KafkaTemplate<String, String> kafkaTemplate;
  private final TopicResolver topicResolver;

  @Override
  public void publish(TopicType topic, String key, String message) {
    kafkaTemplate
        .send(topicResolver.find(topic), key, message)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, String>>() {

              @Override
              public void onSuccess(final SendResult<String, String> message) {
                log.debug(
                    "[Kafka] sent message={} with offset={}",
                    message,
                    message.getRecordMetadata().offset());
              }

              @Override
              public void onFailure(final Throwable throwable) {
                log.error(">>>>> Unable to send message to topic = " + topic, throwable);
              }
            });
  }
}
