package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.dto.InitialDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.Arrays;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class HomeModuleInitialDataAfterSaveListener
    extends BasicInitialDataAfterSaveListener<HomeModule> {

  private InitialDataService service;

  public HomeModuleInitialDataAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HomeModule> event) {
    Arrays.asList("mobile", "tablet", "desktop")
        .forEach(
            deviceType ->
                event
                    .getSource()
                    .getPublishToChannels()
                    .forEach(
                        brand -> {
                          InitialDataDto content =
                              service.fetchInitialData(
                                  brand, deviceType, SegmentConstants.UNIVERSAL);
                          uploadOptional(brand, PATH_TEMPLATE, deviceType, Optional.of(content));
                        }));
  }
}
