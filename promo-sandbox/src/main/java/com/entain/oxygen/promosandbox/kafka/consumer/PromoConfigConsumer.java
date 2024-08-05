package com.entain.oxygen.promosandbox.kafka.consumer;

import com.entain.oxygen.promosandbox.dto.PromoMessageDto;
import com.entain.oxygen.promosandbox.handler.PromoConfigMessageHandler;
import com.google.gson.Gson;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

@Configuration
@Slf4j(topic = "promoConfigConsumer")
public class PromoConfigConsumer {

  private final PromoConfigMessageHandler promoConfigMessageHandler;

  @Autowired
  public PromoConfigConsumer(PromoConfigMessageHandler promoConfigMessageHandler) {
    this.promoConfigMessageHandler = promoConfigMessageHandler;
  }

  @KafkaListener(
      topics = "${promosandbox.topic.promo-config.name}",
      groupId = "${promosandbox.topic.promo-config.groupId}-${random.uuid}",
      concurrency = "${promosandbox.topic.promo-config.concurrency}",
      containerFactory = "kafkaInternalPromoConfigListenerContainerFactory")
  public void consumeRequest(ConsumerRecord<String, String> request) {
    try {
      log.info("Received promo message :: " + request.value());
      promoConfigMessageHandler.handleKafkaMessage(
          new Gson().fromJson(request.value(), PromoMessageDto.class));
    } catch (Exception ex) {
      log.error("Error in promoConfigConsumer : {} ", ex.getMessage());
    }
  }
}
