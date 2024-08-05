package com.ladbrokescoral.oxygen.betpackmp.kafka;

import static com.ladbrokescoral.oxygen.betpackmp.util.DateUtils.scrub;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFutureCallback;

@RequiredArgsConstructor
public class AbstractKafkaPublisher {

  private final KafkaTemplate<String, FreebetOffer> kafkaTemplate;
  private final String topic;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public void publish(String key, FreebetOffer message) {
    ASYNC_LOGGER.info(
        "[Kafka] topic: {} key: {} message: {}",
        scrub(topic),
        scrub(key),
        scrub(message.toString()));
    kafkaTemplate
        .send(topic, key, message)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, FreebetOffer>>() {

              @Override
              public void onSuccess(final SendResult<String, FreebetOffer> message) {
                ASYNC_LOGGER.info(
                    "[Kafka] sent message= {}} with offset= {}",
                    scrub(message.toString()),
                    message.getRecordMetadata().offset());
              }

              @Override
              public void onFailure(final Throwable throwable) {
                ASYNC_LOGGER.error("Unable to send message to topic = {}", scrub(topic), throwable);
              }
            });
  }
}
