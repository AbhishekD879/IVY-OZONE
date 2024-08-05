package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SeasonDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonGamificationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Season;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeasonPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SeasonAfterSaveListener extends BasicMongoEventListener<Season> {
  private final SeasonPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "season";
  private static final String FILE_NAME_V2 = "current-future-seasons";
  private static final String COLLECTION_NAME = "season";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-season}")
  private String ladsSeasonTopic;

  public SeasonAfterSaveListener(
      final SeasonPublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Season> event) {
    String brand = event.getSource().getBrand();

    List<SeasonDto> content = service.findAllByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    /*
     * We have added this api to get today's and future seasons data and this api will be used in
     * BMA for one-two free gamification feature for better performance
     *
     * If Gamification doesn't exist at the current point of time we are only sending season Data
     * and gamification Info null
     */
    List<SeasonGamificationDto> currentFutureSeasons = service.getCurrentFutureSeasons(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME_V2, currentFutureSeasons);
    ladsCoralKafkaPublisher.publishMessage(ladsSeasonTopic, brand, COLLECTION_NAME);
  }
}
