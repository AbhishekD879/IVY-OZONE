package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.YcLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.YourCallLeague;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.YourCallLeaguePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class YcLeagueAfterSaveListener extends BasicMongoEventListener<YourCallLeague> {

  private final YourCallLeaguePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "yc-leagues";
  private static final String COLLECTION_NAME = "ycleagues";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-ycleagues}")
  private String ladsYcleaguesTopic;

  @Value(value = "${coral.kafka.topic.cms-ycleagues}")
  private String coralYcleaguesTopic;

  public YcLeagueAfterSaveListener(
      final YourCallLeaguePublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<YourCallLeague> event) {
    String brand = event.getSource().getBrand();
    List<YcLeagueDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    // cms-push mechanism implementation
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralYcleaguesTopic : ladsYcleaguesTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
