package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.Fanzone;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzonesAfterSaveListener extends BasicMongoEventListener<Fanzone> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone";
  private static final String COLLECTION_NAME = "fanzone";
  private final FanzonesService service;
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-fanzones}")
  private String ladsFanzoneTopic;

  @Value(value = "${coral.kafka.topic.cms-fanzones}")
  private String coralFanzoneTopic;

  public FanzonesAfterSaveListener(
      final FanzonesService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Fanzone> event) {
    String brand = event.getSource().getBrand();
    log.info("Fanzones storing at s3 bucket{}", brand);
    List<Fanzone> fanzone = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzone);
    // cms-push mechanism implementation
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralFanzoneTopic : ladsFanzoneTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
