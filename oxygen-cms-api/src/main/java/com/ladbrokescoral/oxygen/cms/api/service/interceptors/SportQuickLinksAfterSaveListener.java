package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportQuickLinkPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Slf4j
@Component
public class SportQuickLinksAfterSaveListener extends BasicMongoEventListener<SportQuickLink> {

  private final SportQuickLinkPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "sport-quick-links";
  private static final String COLLECTION_NAME = "sportquicklinks";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportquicklinks}")
  private String ladsSportquicklinksTopic;

  @Value(value = "${coral.kafka.topic.cms-sportquicklinks}")
  private String coralSportquicklinksTopic;

  public SportQuickLinksAfterSaveListener(
      final SportQuickLinkPublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SportQuickLink> event) {
    if (!ObjectUtils.isEmpty(event)) {
      String brand = event.getSource().getBrand();
      List<SportQuickLinkDto> content = service.findAll(brand);
      uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
      String topic =
          brand.equalsIgnoreCase(Brand.BMA) ? coralSportquicklinksTopic : ladsSportquicklinksTopic;
      ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
    }
  }
}
