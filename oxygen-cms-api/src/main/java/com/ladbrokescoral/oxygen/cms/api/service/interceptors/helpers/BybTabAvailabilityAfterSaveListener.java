package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.entity.BybTabAvailability;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BybTabAvailabilityAfterSaveListener
    extends BasicInitialDataAfterSaveListener<BybTabAvailability> {

  public BybTabAvailabilityAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BybTabAvailability> event) {
    upload(event);
  }
}
