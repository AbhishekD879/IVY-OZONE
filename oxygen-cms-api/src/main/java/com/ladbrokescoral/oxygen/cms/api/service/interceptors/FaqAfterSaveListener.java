package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FaqPublicService;
import java.util.List;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class FaqAfterSaveListener extends BasicMongoEventListener<Faq> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "faq";
  private final FaqPublicService service;

  public FaqAfterSaveListener(
      final FaqPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  /** Method that captures After save event and upload that collection to s3 bucket. */
  @Override
  public void onAfterSave(AfterSaveEvent<Faq> event) {
    String brand = event.getSource().getBrand();
    List<Faq> faq = service.findByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, faq);
  }
}
