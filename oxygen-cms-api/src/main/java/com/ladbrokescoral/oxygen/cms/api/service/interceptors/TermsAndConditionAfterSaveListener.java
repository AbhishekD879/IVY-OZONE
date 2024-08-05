package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.TermsAndConditionPublicService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class TermsAndConditionAfterSaveListener extends BasicMongoEventListener<TermsAndCondition> {
  private static final String PATH_TEMPLATE = "api/{0}";
  private static final String FILE_NAME = "termsandcondition";
  private final TermsAndConditionPublicService service;

  public TermsAndConditionAfterSaveListener(
      final TermsAndConditionPublicService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  /** Method that captures After save event and upload that collection to s3 bucket. */
  @Override
  public void onAfterSave(AfterSaveEvent<TermsAndCondition> event) {
    String brand = event.getSource().getBrand();
    Optional<TermsAndCondition> termsAndCondition = service.findOneByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, termsAndCondition);
  }
}
