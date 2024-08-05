package com.entain.oxygen.kafka;

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

@Slf4j
@RequiredArgsConstructor
public class AbstractKafkaPublisher {

  private final KafkaTemplate<String, String> kafkaTemplate;
  private final String topic;

  public void publishMessage(String key, String message, Optional<Map<String, String>> headersMap) {
    log.info("Publisher topic: {} key: {} ", topic, key);
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
    kafkaTemplate.send(producerRecord);
  }
}
