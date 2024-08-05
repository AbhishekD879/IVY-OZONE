package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.TimelineConfigPublicService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class TimelineSplashConfigAfterSaveListener
    extends BasicMongoEventListener<TimelineSplashConfig> {
  private final TimelineConfigPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "timeline-splash-config";

  public TimelineSplashConfigAfterSaveListener(
      final DeliveryNetworkService deliveryNetworkService,
      final TimelineConfigPublicService service) {
    super(deliveryNetworkService);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<TimelineSplashConfig> event) {
    String brand = event.getSource().getBrand();
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, service.findSplashConfigByBrand(brand));
  }
}
