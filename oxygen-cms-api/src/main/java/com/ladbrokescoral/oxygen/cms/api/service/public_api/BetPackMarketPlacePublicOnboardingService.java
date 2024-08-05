package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceOnboardingService;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

@Service
public class BetPackMarketPlacePublicOnboardingService {
  private BetPackMarketPlaceOnboardingService onboardingService;

  public BetPackMarketPlacePublicOnboardingService(
      BetPackMarketPlaceOnboardingService onboardingService) {
    this.onboardingService = onboardingService;
  }

  public List<BetPackOnboarding> getBpmpOnboardingByBrand(@PathVariable String brand) {
    return onboardingService.findByBrand(brand);
  }
}
