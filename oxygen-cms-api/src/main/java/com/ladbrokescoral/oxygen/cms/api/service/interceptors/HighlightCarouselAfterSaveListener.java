package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class HighlightCarouselAfterSaveListener extends BasicMongoEventListener<HighlightCarousel> {
  private static final String COLLECTION_NAME = "highlightCarousel";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-highlightCarousel}")
  private String ladsHighlightCarouselTopic;

  @Value(value = "${coral.kafka.topic.cms-highlightCarousel}")
  private String coralHighlightCarouselTopic;

  public HighlightCarouselAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HighlightCarousel> event) {
    String brand = event.getSource().getBrand();
    String topic =
        brand.equalsIgnoreCase(Brand.BMA)
            ? coralHighlightCarouselTopic
            : ladsHighlightCarouselTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
