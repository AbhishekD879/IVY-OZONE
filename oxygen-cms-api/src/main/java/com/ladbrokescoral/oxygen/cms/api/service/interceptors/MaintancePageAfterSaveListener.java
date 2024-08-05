package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.MaintenancePageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.MaintenancePagePublicService;
import java.util.Arrays;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class MaintancePageAfterSaveListener extends BasicMongoEventListener<MaintenancePage> {

  private final MaintenancePagePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/maintenance-page";

  public MaintancePageAfterSaveListener(
      final MaintenancePagePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<MaintenancePage> event) {

    Arrays.asList("mobile", "tablet", "desktop")
        .forEach(
            deviceType -> {
              String brand = event.getSource().getBrand();
              List<MaintenancePageDto> content = service.findMaintenanePages(brand, deviceType);
              uploadCollection(brand, PATH_TEMPLATE, deviceType, content);
            });
  }
}
