package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PopularAccaWidgetPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class PopularAccaWidgetAfterSaveListener extends BasicMongoEventListener<PopularAccaWidget> {

  private final PopularAccaWidgetPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "popular-acca-widgets";

  public PopularAccaWidgetAfterSaveListener(
      PopularAccaWidgetPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<PopularAccaWidget> event) {
    String brand = event.getSource().getBrand();
    Optional<PopularAccaWidgetDto> content = service.readByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
