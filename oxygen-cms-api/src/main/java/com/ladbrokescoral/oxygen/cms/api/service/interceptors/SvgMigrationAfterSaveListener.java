package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgMigration;
import com.ladbrokescoral.oxygen.cms.api.service.SvgMigrationService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SvgMigrationAfterSaveListener extends BasicMongoEventListener<SvgMigration> {

  private final SvgMigrationService service;

  public SvgMigrationAfterSaveListener(
      DeliveryNetworkService deliveryservice, SvgMigrationService service) {
    super(deliveryservice);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SvgMigration> event) {
    super.onAfterSave(event);
    service.process(event.getSource());
  }
}
