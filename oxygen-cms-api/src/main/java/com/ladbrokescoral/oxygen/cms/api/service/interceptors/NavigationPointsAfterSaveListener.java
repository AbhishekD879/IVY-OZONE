package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationPointService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class NavigationPointsAfterSaveListener extends BasicMongoEventListener<NavigationPoint> {

  private final NavigationPointService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "navigation-points";
  private static final String COLLECTION_NAME = "navigationPoint";

  public NavigationPointsAfterSaveListener(
      NavigationPointService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<NavigationPoint> event) {
    if (COLLECTION_NAME.equals(event.getCollectionName())) {
      String brand = event.getSource().getBrand();
      List<NavigationPointDto> content = service.getNavigationPointByBrandEnabled(brand);
      uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);
    }
  }
}
