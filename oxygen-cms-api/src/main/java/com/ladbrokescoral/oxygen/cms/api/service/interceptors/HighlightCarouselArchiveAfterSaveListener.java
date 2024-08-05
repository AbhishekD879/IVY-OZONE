package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.entity.HighlightCarouselArchive;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class HighlightCarouselArchiveAfterSaveListener
    extends BasicMongoEventListener<HighlightCarouselArchive> {
  private static final String COLLECTION_NAME = "highlightCarouselArchive";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-highlightCarouselArchive}")
  private String ladsHighlightCarouselArchiveTopic;

  @Value(value = "${coral.kafka.topic.cms-highlightCarouselArchive}")
  private String coralHighlightCarouselArchiveTopic;

  public HighlightCarouselArchiveAfterSaveListener(
      DeliveryNetworkService context, LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HighlightCarouselArchive> event) {
    String brand = event.getSource().getBrand();
    String topic =
        brand.equalsIgnoreCase(Brand.BMA)
            ? coralHighlightCarouselArchiveTopic
            : ladsHighlightCarouselArchiveTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
