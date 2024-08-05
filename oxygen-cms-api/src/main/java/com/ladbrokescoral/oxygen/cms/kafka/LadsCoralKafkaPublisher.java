package com.ladbrokescoral.oxygen.cms.kafka;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Slf4j
@Component
public class LadsCoralKafkaPublisher {
  private final KafkaTemplate<String, String> coralKafkaTemplate;
  private final KafkaTemplate<String, String> ladbrokesKafkaTemplate;

  public LadsCoralKafkaPublisher(
      KafkaTemplate<String, String> coralKafkaTemplate,
      KafkaTemplate<String, String> ladbrokesKafkaTemplate) {
    this.coralKafkaTemplate = coralKafkaTemplate;
    this.ladbrokesKafkaTemplate = ladbrokesKafkaTemplate;
  }

  @Async
  public void publishMessage(String topic, String brand, String collection) {
    log.debug(
        "Publishing message to Kafka topic: {} for brand: {} for collection : {}",
        topic,
        brand,
        collection);
    getKafkaTemplateByBrand(brand)
        .send(topic, brand, collection)
        .addCallback(
            new ListenableFutureCallback<SendResult<String, String>>() {
              @Override
              public void onSuccess(SendResult<String, String> result) {
                log.info(
                    "Kafka message publish successfully with brand : {} , in topic: {}",
                    brand,
                    topic);
              }

              @Override
              public void onFailure(Throwable ex) {
                log.error(
                    "Error while publishing CMS Push kafka message: {},error: {}, in topic: {}",
                    brand,
                    ex.getMessage(),
                    topic);
              }
            });
  }

  private KafkaTemplate<String, String> getKafkaTemplateByBrand(String brand) {
    return brand.equalsIgnoreCase(Brand.BMA) ? coralKafkaTemplate : ladbrokesKafkaTemplate;
  }
}
