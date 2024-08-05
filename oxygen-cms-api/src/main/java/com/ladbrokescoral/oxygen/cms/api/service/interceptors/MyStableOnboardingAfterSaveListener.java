package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.MyStableOnboardingCFDto;
import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.MyStableOnboardingService;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class MyStableOnboardingAfterSaveListener
    extends BasicMongoEventListener<MyStableOnboarding> {
  private final MyStableOnboardingService service;
  private static final String PATH_TEMPLATE = "api/{0}/my-stable";
  private static final String FILE_NAME = "onboarding";

  public MyStableOnboardingAfterSaveListener(
      final MyStableOnboardingService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<MyStableOnboarding> event) {
    String brand = event.getSource().getBrand();
    Optional<MyStableOnboardingCFDto> content = service.convertToCFDto(event.getSource());
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
  }
}
