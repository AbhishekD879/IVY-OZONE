package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FeatureContainerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FeaturePublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FeaturesAfterSaveListener extends BasicMongoEventListener<Feature> {
  private final FeaturePublicService featureService;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "features";

  public FeaturesAfterSaveListener(
      final FeaturePublicService featureService, final DeliveryNetworkService context) {
    super(context);
    this.featureService = featureService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Feature> event) {
    String brand = event.getSource().getBrand();
    FeatureContainerDto content = featureService.findContainerByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, Optional.of(content));
  }
}
