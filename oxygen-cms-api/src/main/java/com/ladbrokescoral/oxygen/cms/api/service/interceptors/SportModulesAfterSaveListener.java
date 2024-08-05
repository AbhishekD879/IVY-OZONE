package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportModulesAfterSaveListener extends BasicMongoEventListener<SportModule> {
  private static final String COLLECTION_NAME = "sportmodules";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportModules}")
  private String ladsSportModulesTopic;

  @Value(value = "${coral.kafka.topic.cms-sportModules}")
  private String coralSportModulesTopic;

  public SportModulesAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SportModule> event) {
    String brand = event.getSource().getBrand();
    String topic =
        brand.equalsIgnoreCase(Brand.BMA) ? coralSportModulesTopic : ladsSportModulesTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
