package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OverlayPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class OverlayAftersaveListener extends BasicMongoEventListener<Overlay> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "overlay";
  private final OverlayPublicService service;

  public OverlayAftersaveListener(
      final OverlayPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  /** Method that captures After save event and upload that collection to s3 bucket. */
  @Override
  public void onAfterSave(AfterSaveEvent<Overlay> event) {
    String brand = event.getSource().getBrand();
    Optional<Overlay> overlayInfo = service.findOneByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, overlayInfo);
  }
}
