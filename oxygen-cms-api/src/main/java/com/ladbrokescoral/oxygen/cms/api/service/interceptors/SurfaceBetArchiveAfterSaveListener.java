package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.SurfaceBetArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SurfaceBetArchiveAfterSaveListener extends BasicMongoEventListener<SurfaceBetArchive> {
  private static final String COLLECTION_NAME = "surfacebetArchive";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-surfacebetArchive}")
  private String ladsSurfacebetArchiveTopic;

  @Value(value = "${coral.kafka.topic.cms-surfacebetArchive}")
  private String coralSurfacebetArchiveTopic;

  public SurfaceBetArchiveAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SurfaceBetArchive> event) {
    String brand = event.getSource().getBrand();
    String topic =
        brand.equalsIgnoreCase(Brand.BMA)
            ? coralSurfacebetArchiveTopic
            : ladsSurfacebetArchiveTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
