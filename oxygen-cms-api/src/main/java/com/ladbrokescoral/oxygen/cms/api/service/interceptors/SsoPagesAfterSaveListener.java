package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.SsoPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SsoPagePublicService;
import java.util.Arrays;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SsoPagesAfterSaveListener extends BasicMongoEventListener<SsoPage> {

  private final SsoPagePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/sso-page";

  public SsoPagesAfterSaveListener(
      final SsoPagePublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SsoPage> event) {
    Arrays.asList("ios", "android")
        .forEach(
            osType -> {
              String brand = event.getSource().getBrand();
              List<SsoPageDto> content = service.findByBrand(brand, osType);
              uploadCollection(brand, PATH_TEMPLATE, osType, content);
            });
  }
}
