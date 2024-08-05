package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderSubMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderSubMenu;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.HeaderSubMenuPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class HeaderSubMenuAfterSaveListener extends BasicMongoEventListener<HeaderSubMenu> {

  private final HeaderSubMenuPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "header-submenu";

  public HeaderSubMenuAfterSaveListener(
      final HeaderSubMenuPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HeaderSubMenu> event) {
    String brand = event.getSource().getBrand();
    List<HeaderSubMenuDto> content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
