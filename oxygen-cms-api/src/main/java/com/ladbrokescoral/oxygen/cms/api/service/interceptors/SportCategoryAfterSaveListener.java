package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import static com.ladbrokescoral.oxygen.cms.util.Util.isOneOf;
import static java.util.Objects.nonNull;

import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class SportCategoryAfterSaveListener extends BasicMongoEventListener<SportCategory> {

  private final SportCategoryPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "sport-category";
  private static final String CONFIGS_PATH_TEMPLATE = "api/{0}/sport-config";
  private static final String COLLECTION_NAME = "sportcategories";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportcategories}")
  private String ladsSportcategoriesTopic;

  @Value(value = "${coral.kafka.topic.cms-sportcategories}")
  private String coralSportcategoriesTopic;

  public SportCategoryAfterSaveListener(
      final SportCategoryPublicService service,
      DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SportCategory> event) {
    if (COLLECTION_NAME.equals(event.getCollectionName())) {
      upload(event);
    }
  }

  private void upload(AfterSaveEvent<SportCategory> event) {
    uploadCategory(event);
    SportCategory category = event.getSource();
    if (canUploadConfig(category)) {
      String brand = event.getSource().getBrand();
      Integer sportId = event.getSource().getCategoryId();
      uploadOptional(
          brand,
          CONFIGS_PATH_TEMPLATE,
          sportId.toString(),
          Optional.of(service.getSportConfig(brand, sportId)));
      String topic =
          brand.equalsIgnoreCase(Brand.BMA) ? coralSportcategoriesTopic : ladsSportcategoriesTopic;
      ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
    }
  }

  private boolean canUploadConfig(SportCategory category) {
    return nonNull(category.getCategoryId())
        && isOneOf(category.getTier(), SportTier.TIER_1, SportTier.TIER_2);
  }

  private void uploadCategory(AfterSaveEvent<SportCategory> event) {
    String brand = event.getSource().getBrand();
    List<SportCategoryDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }

  @Override
  public void onAfterDelete(AfterDeleteEvent<SportCategory> deleteEvent) {
    String sportId = deleteEvent.getSource().getString("categoryId");
    String brand = deleteEvent.getSource().getString("brand");
    delete(brand, CONFIGS_PATH_TEMPLATE, sportId);
  }
}
