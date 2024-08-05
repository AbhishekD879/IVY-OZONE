package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.WidgetPublicService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class WidgetsAfterSaveListener extends BasicMongoEventListener<Widget> {
  private final WidgetPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "widgets";

  public WidgetsAfterSaveListener(
      final WidgetPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Widget> event) {
    String brand = event.getSource().getBrand();
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, service.findByBrand(brand));
  }
}
