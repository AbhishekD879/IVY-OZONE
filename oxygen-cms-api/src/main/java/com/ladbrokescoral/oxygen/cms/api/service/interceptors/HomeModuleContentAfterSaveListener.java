package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ModularContentPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Slf4j
@Component
public class HomeModuleContentAfterSaveListener extends BasicMongoEventListener<HomeModule> {

  private final ModularContentPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "modular-content";
  private static final String COLLECTION_NAME = "homemodules";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-homemodules}")
  private String ladsHomemodulesTopic;

  @Value(value = "${coral.kafka.topic.cms-homemodules}")
  private String coralHomemodulesTopic;

  public HomeModuleContentAfterSaveListener(
      final ModularContentPublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HomeModule> event) {
    if (!ObjectUtils.isEmpty(event)) {
      for (String brand : event.getSource().getPublishToChannels()) {
        List<BaseModularContentDto> content = service.findByBrand(brand);
        uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
        String topic =
            brand.equalsIgnoreCase(Brand.BMA) ? coralHomemodulesTopic : ladsHomemodulesTopic;
        ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
      }
    }
  }
}
