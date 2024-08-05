package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavigationGroupPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class NavigationGroupAfterSaveListener extends BasicMongoEventListener<NavigationGroup> {
  private final NavigationGroupPublicService navigationGroupPublicService;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILENAME = "navigation-group";

  public NavigationGroupAfterSaveListener(
      DeliveryNetworkService context, NavigationGroupPublicService navigationGroupPublicService) {
    super(context);
    this.navigationGroupPublicService = navigationGroupPublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<NavigationGroup> event) {
    String brand = event.getSource().getBrand();
    List<NavigationGroupPublicDto> content =
        navigationGroupPublicService.getNavigationGroupByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILENAME, content);
  }
}
