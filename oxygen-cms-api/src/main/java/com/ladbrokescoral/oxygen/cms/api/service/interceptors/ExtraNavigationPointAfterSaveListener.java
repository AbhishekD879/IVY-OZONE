package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.ExtraNavigationPointPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ExtraNavigationPointPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class ExtraNavigationPointAfterSaveListener
    extends BasicMongoEventListener<ExtraNavigationPoint> {
  private final ExtraNavigationPointPublicService navigationPointPublicService;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "extra-navigation-points";

  protected ExtraNavigationPointAfterSaveListener(
      DeliveryNetworkService context,
      ExtraNavigationPointPublicService navigationPointPublicService) {
    super(context);
    this.navigationPointPublicService = navigationPointPublicService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<ExtraNavigationPoint> event) {
    String brand = event.getSource().getBrand();
    List<ExtraNavigationPointPublicDto> extraNavigationPoints =
        navigationPointPublicService.findAllActiveExtraNavPointsByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, extraNavigationPoints);
  }
}
