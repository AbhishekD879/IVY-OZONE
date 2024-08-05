package com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers;

import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class NavigationPointsInitialDataAfterSaveListener
    extends BasicInitialDataAfterSaveListener<NavigationPoint> {
  private static final String COLLECTION_NAME = "navigationPoint";

  public NavigationPointsInitialDataAfterSaveListener(
      InitialDataService service, DeliveryNetworkService context) {
    super(service, context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<NavigationPoint> event) {
    if (COLLECTION_NAME.equals(event.getCollectionName())) {
      upload(event);
    }
  }
}
