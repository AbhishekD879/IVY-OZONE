package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentedModule;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SegmentedModuleAfterSaveListener extends BasicMongoEventListener<SegmentedModule> {
  private static final String COLLECTION_NAME = "segmentedModules";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-segmentedModules}")
  private String ladsSegmentedModulesTopic;

  @Value(value = "${coral.kafka.topic.cms-segmentedModules}")
  private String coralSegmentedModulesTopic;

  public SegmentedModuleAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SegmentedModule> event) {
    String brand = event.getSource().getBrand();
    String topic =
        brand.equalsIgnoreCase(Brand.BMA) ? coralSegmentedModulesTopic : ladsSegmentedModulesTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
