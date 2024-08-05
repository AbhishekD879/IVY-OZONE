package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicOnboardingService;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class BetPackOnboardingAfterSaveListener extends BasicMongoEventListener<BetPackOnboarding> {

  private final BetPackMarketPlacePublicOnboardingService betPackMarketPlacePublicOnboardingService;

  private static final String PATH_TEMPLATE = "api/{0}/bet-pack";

  private static final String FILE_NAME = "onboarding";

  public BetPackOnboardingAfterSaveListener(
      DeliveryNetworkService context,
      BetPackMarketPlacePublicOnboardingService betPackMarketPlacePublicOnboardingService) {
    super(context);
    this.betPackMarketPlacePublicOnboardingService = betPackMarketPlacePublicOnboardingService;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetPackOnboarding> event) {
    String brand = event.getSource().getBrand();
    List<BetPackOnboarding> content =
        betPackMarketPlacePublicOnboardingService.getBpmpOnboardingByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, Optional.of(content.get(0)));
  }
}
