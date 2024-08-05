package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.HeaderContactMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.HeaderContactMenuPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class HeaderContactMenuAfterSaveListener extends BasicMongoEventListener<HeaderContactMenu> {

  private final HeaderContactMenuPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "header-contact-menu";

  public HeaderContactMenuAfterSaveListener(
      final HeaderContactMenuPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<HeaderContactMenu> event) {
    String brand = event.getSource().getBrand();
    List<HeaderContactMenuDto> content = service.find(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
