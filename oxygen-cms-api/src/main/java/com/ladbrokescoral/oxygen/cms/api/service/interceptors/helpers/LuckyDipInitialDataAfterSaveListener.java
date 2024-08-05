package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class LuckyDipInitialDataAfterSaveListener
    extends BasicInitialDataAfterSaveListener<LuckyDipV2Config> {

  public LuckyDipInitialDataAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<LuckyDipV2Config> event) {
    upload(event);
  }
}
