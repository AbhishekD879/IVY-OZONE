package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;

public class AbstractSportTabAfterSaveListener<T extends HasBrand>
    extends BasicMongoEventListener<T> {
  private final SportCategoryPublicService sportPublicService;
  protected static final String PATH_TEMPLATE = "api/{0}/sport-tabs";
  protected static final String CONFIGS_PATH_TEMPLATE = "api/{0}/sport-config";
  private static final String COLLECTION_NAME = "sporttabs";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-sporttabs}")
  private String ladsSporttabsTopic;

  @Value(value = "${coral.kafka.topic.cms-sporttabs}")
  private String coralSporttabsTopic;

  public AbstractSportTabAfterSaveListener(
      final SportCategoryPublicService sportPublicService,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.sportPublicService = sportPublicService;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  public void uploadSportTabs(Integer sportId, String brand) {
    uploadTabs(sportId, brand);
    /*
     Because sport-tabs were previously part of sport-category,
     we still need to upload them for backward-compatibility.
     Once UI is fully migrated to use sport-tabs public api, this can be deleted.
    */
    uploadConfigs(sportId, brand);
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralSporttabsTopic : ladsSporttabsTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }

  private void uploadTabs(Integer sportId, String brand) {
    uploadOptional(
        brand,
        PATH_TEMPLATE,
        sportId.toString(),
        Optional.of(sportPublicService.getSportTabs(brand, sportId)));
  }

  private void uploadConfigs(Integer sportId, String brand) {
    uploadOptional(
        brand,
        CONFIGS_PATH_TEMPLATE,
        sportId.toString(),
        Optional.of(sportPublicService.getSportConfig(brand, sportId)));
  }
}
