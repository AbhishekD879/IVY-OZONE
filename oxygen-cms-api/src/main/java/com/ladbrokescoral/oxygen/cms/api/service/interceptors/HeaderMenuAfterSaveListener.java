package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.HeaderMenuPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class HeaderMenuAfterSaveListener extends BasicMongoEventListener<HeaderMenu> {

  private final HeaderMenuPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "header-menu";

  public HeaderMenuAfterSaveListener(
      final HeaderMenuPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HeaderMenu> event) {
    String brand = event.getSource().getBrand();
    List<HeaderMenuDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
