package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryNativeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportCategoryNativeAfterSaveListener extends BasicMongoEventListener<SportCategory> {

  private final SportCategoryPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "sport-category-native";
  private static final String COLLECTION_NAME = "sportcategories";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportcategories}")
  private String ladsSportcategoriesTopic;

  @Value(value = "${coral.kafka.topic.cms-sportcategories}")
  private String coralSportcategoriesTopic;

  public SportCategoryNativeAfterSaveListener(
      final SportCategoryPublicService service,
      DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SportCategory> event) {
    String brand = event.getSource().getBrand();
    List<SportCategoryNativeDto> content = service.findNative(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    // cms-push mechanism implementation
    String topic =
        brand.equalsIgnoreCase(Brand.BMA) ? coralSportcategoriesTopic : ladsSportcategoriesTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
