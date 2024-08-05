package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.entity.StaticBlock;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class StaticBlockInitialDataAfterSaveListener
    extends BasicInitialDataAfterSaveListener<StaticBlock> {
  public StaticBlockInitialDataAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<StaticBlock> event) {
    upload(event);
  }
}
