package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import com.ladbrokescoral.oxygen.cms.api.service.InitialDataService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.helpers.BasicInitialDataAfterSaveListener;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SeoAutoPageAftersaveListener extends BasicInitialDataAfterSaveListener<SeoAutoPage> {

  public SeoAutoPageAftersaveListener(
      final InitialDataService initialDataService,
      final DeliveryNetworkService deliveryNetworkService) {
    super(initialDataService, deliveryNetworkService);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SeoAutoPage> event) {
    super.upload(event);
  }
}
