package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class TimelineConfigAfterSaveListener extends BasicInitialDataAfterSaveListener<Config> {
  public TimelineConfigAfterSaveListener(
      final InitialDataService initialDataService,
      final DeliveryNetworkService deliveryNetworkService) {
    super(initialDataService, deliveryNetworkService);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Config> event) {
    super.upload(event);
  }
}
