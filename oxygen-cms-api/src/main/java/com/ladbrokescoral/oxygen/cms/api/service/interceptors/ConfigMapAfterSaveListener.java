package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class ConfigMapAfterSaveListener extends BasicMongoEventListener<ApiCollectionConfig> {

  private static final String COLLECTION_NAME = "configMap";

  @Value(value = "${ladbrokes.kafka.topic.cms-config-map}")
  private String ladsConfigMapTopic;

  @Value(value = "${coral.kafka.topic.cms-config-map}")
  private String coralConfigMapTopic;

  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  public ConfigMapAfterSaveListener(
      final DeliveryNetworkService context, final LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<ApiCollectionConfig> event) {
    String brand = event.getSource().getBrand();
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralConfigMapTopic : ladsConfigMapTopic;
    log.info(
        "Publishing ConfigMap update for collection: {} with brand: {} to kafka cluster ",
        COLLECTION_NAME,
        brand);
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
