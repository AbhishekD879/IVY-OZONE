package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDetailsPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonGamificationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeasonPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class GamificationAfterSaveListener extends BasicMongoEventListener<Gamification> {

  private final GamificationPublicService gamificationPublicService;
  private final SeasonPublicService seasonPublicService;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "gamification";
  private static final String FILE_NAME_V2 = "current-future-seasons";
  private static final String COLLECTION_NAME = "gamification";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-gamification}")
  private String ladsGamificationTopic;

  public GamificationAfterSaveListener(
      final GamificationPublicService gamificationPublicService,
      final SeasonPublicService seasonPublicService,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.seasonPublicService = seasonPublicService;
    this.gamificationPublicService = gamificationPublicService;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Gamification> event) {
    String brand = event.getSource().getBrand();
    List<GamificationDetailsPublicDto> content =
        gamificationPublicService.findGamificationByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    /*
     * We have added this api to get today's and future seasons data and this api will be used in
     * BMA for one-two free gamification feature for better performance
     *
     * When gamification is created, we are pushing gamification data along with season info
     * already pushed at the time of season creation
     */
    List<SeasonGamificationDto> currentFutureSeasons =
        seasonPublicService.getCurrentFutureSeasons(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME_V2, currentFutureSeasons);
    ladsCoralKafkaPublisher.publishMessage(ladsGamificationTopic, brand, COLLECTION_NAME);
  }
}
