package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavItemPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class NavItemAfterSaveListener extends BasicMongoEventListener<NavItem> {
  private final NavItemPublicService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILENAME = "navigation-group";

  public NavItemAfterSaveListener(
      final NavItemPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<NavItem> event) {
    String brand = event.getSource().getBrand();
    List<NavigationGroupPublicDto> navigationGroupPublicDtoList =
        service.getNavigationGroupByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILENAME, navigationGroupPublicDtoList);
  }
}
