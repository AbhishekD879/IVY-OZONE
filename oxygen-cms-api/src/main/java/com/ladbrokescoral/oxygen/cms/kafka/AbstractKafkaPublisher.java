package com.ladbrokescoral.oxygen.cms.kafka;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.header.Header;
import org.apache.kafka.common.header.internals.RecordHeader;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Slf4j
@RequiredArgsConstructor
public class AbstractKafkaPublisher {
  private final KafkaTemplate<String, String> ladbrokesKafkaTemplate;
  private final String topic;

  public void publish(String key, String message, Optional<Map<String, String>> headersMap) {
    log.info("Contest [Kafka] topic: {} key: {} ", topic, key);
    List<Header> headers = new ArrayList<>();
    headersMap.ifPresent(
        (Map<String, String> headerMap) ->
            headerMap.forEach(
                (String headerKey, String headerValue) -> {
                  Header header = new RecordHeader(headerKey, headerValue.getBytes());
                  headers.add(header);
                }));
    ProducerRecord<String, String> producerRecord =
        new ProducerRecord<>(topic, null, null, key, message, headers);
    ladbrokesKafkaTemplate
        .send(producerRecord)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, String>>() {

              @Override
              public void onSuccess(final SendResult<String, String> message) {
                log.info(
                    "Contest [Kafka] sent message= {}} with offset= {}",
                    message,
                    message.getRecordMetadata().offset());
              }

              @Override
              public void onFailure(final Throwable throwable) {
                log.error("Contest Unable to send message to topic = " + topic, throwable);
              }
            });
  }
}
