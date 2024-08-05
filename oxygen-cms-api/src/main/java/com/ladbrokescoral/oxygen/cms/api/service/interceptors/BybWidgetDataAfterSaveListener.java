package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybWidgetPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BybWidgetDataAfterSaveListener extends BasicMongoEventListener<BybWidgetData> {

  private final BybWidgetPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "byb-widgets";

  public BybWidgetDataAfterSaveListener(
      BybWidgetPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BybWidgetData> event) {
    String brand = event.getSource().getBrand();
    Optional<BybWidgetDto> content = service.readByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
