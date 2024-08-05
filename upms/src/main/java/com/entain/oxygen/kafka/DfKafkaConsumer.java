package com.entain.oxygen.kafka;

import com.entain.oxygen.service.RtmsKafkaPublisherService;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@ConditionalOnProperty(value = "upms_kafka.enabled", havingValue = "true", matchIfMissing = true)
public class DfKafkaConsumer {

  RtmsKafkaPublisherService rtmsKafkaPublisherService;

  public DfKafkaConsumer(RtmsKafkaPublisherService rtmsKafkaPublisherService) {
    this.rtmsKafkaPublisherService = rtmsKafkaPublisherService;
  }

  @KafkaListener(
      topics = "${df.fanzone-player-preferences}",
      containerFactory = "filteredKafkaContainerFactory")
  public void consumeUpdate(ConsumerRecord<String, String> dfUpdate)
      throws JsonProcessingException {
    log.info(
        " df-fanzone-player-preferences topic :: "
            + dfUpdate.topic()
            + " key :: "
            + dfUpdate.key()
            + " value :: "
            + dfUpdate.value());
    rtmsKafkaPublisherService.processMessage(dfUpdate);
  }
}
