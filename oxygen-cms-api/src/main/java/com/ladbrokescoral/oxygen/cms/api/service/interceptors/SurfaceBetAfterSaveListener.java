package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SurfaceBetAfterSaveListener extends BasicMongoEventListener<SurfaceBet> {
  private static final String COLLECTION_NAME = "surfaceBet";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-surfaceBet}")
  private String ladsSurfaceBetTopic;

  @Value(value = "${coral.kafka.topic.cms-surfaceBet}")
  private String coralSurfaceBetTopic;

  public SurfaceBetAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SurfaceBet> event) {
    String brand = event.getSource().getBrand();
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralSurfaceBetTopic : ladsSurfaceBetTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
