package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportsAfterSaveListener extends BasicMongoEventListener<Sport> {

  private final SportPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "sports";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  private static final String COLLECTION_NAME = "sports";

  @Value(value = "${ladbrokes.kafka.topic.cms-sports}")
  private String ladsSportsTopic;

  @Value(value = "${coral.kafka.topic.cms-sports}")
  private String coralSportsTopic;

  public SportsAfterSaveListener(
      SportPublicService service,
      DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Sport> event) {
    String brand = event.getSource().getBrand();
    List<SportDto> content = service.find(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralSportsTopic : ladsSportsTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
