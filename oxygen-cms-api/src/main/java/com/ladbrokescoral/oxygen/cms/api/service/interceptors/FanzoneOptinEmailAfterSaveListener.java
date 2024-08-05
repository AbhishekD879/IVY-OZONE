package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FanzoneOptinEmailAfterSaveListener extends BasicMongoEventListener<FanzoneOptinEmail> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "fanzone-optin-email";
  private final FanzonesOptinEmailService service;

  public FanzoneOptinEmailAfterSaveListener(
      final FanzonesOptinEmailService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<FanzoneOptinEmail> event) {
    String brand = event.getSource().getBrand();
    log.info("Fanzone optin email storing at s3 bucket{}", brand);
    List<FanzoneOptinEmail> fanzoneOptinEmail = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, fanzoneOptinEmail);
  }
}
