package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.GameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.GamePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class GameAfterSaveListener extends BasicMongoEventListener<Game> {
  private final GamePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "games";
  private static final String COLLECTION_NAME = "games";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-games}")
  private String ladsGamesTopic;

  public GameAfterSaveListener(
      final GamePublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Game> event) {
    String brand = event.getSource().getBrand();
    List<GameDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    ladsCoralKafkaPublisher.publishMessage(ladsGamesTopic, brand, COLLECTION_NAME);
  }
}
