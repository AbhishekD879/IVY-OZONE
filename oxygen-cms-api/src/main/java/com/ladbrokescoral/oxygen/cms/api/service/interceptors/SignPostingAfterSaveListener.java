package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import com.ladbrokescoral.oxygen.cms.api.service.SignPostingService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class SignPostingAfterSaveListener extends BasicMongoEventListener<SignPosting> {
  private final SignPostingService service;
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "signposting";

  public SignPostingAfterSaveListener(
      final SignPostingService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<SignPosting> event) {
    String brand = event.getSource().getBrand();
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, service.findAllByBrand(brand));
  }
}
