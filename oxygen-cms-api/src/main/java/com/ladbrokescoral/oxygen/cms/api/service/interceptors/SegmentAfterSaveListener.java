package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SegmentAfterSaveListener extends BasicMongoEventListener<Segment> {
  private static final String COLLECTION_NAME = "segments";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-segments}")
  private String ladsSegmentsTopic;

  @Value(value = "${coral.kafka.topic.cms-segments}")
  private String coralSegmentsTopic;

  public SegmentAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Segment> event) {
    String brand = event.getSource().getBrand();
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralSegmentsTopic : ladsSegmentsTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
