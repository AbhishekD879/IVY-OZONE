package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfIosAppToggleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfIosAppToggle;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfIosAppTogglePublicService;
import java.util.Collections;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class OtfIosToggleAfterSaveListener extends BasicMongoEventListener<OtfIosAppToggle> {

  private final OtfIosAppTogglePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "otf-ios-app-toggle";

  public OtfIosToggleAfterSaveListener(
      OtfIosAppTogglePublicService service, DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<OtfIosAppToggle> event) {
    String brand = event.getSource().getBrand();
    OtfIosAppToggleDto content = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, Collections.singletonList(content));
  }
}
