package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackOnboarding;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicOnboardingService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BetPackMarketPlaceOnboardingApi implements Public {

  private BetPackMarketPlacePublicOnboardingService betPackMarketPlaceOnboardingService;

  public BetPackMarketPlaceOnboardingApi(
      BetPackMarketPlacePublicOnboardingService betPackMarketPlaceOnboardingService) {
    this.betPackMarketPlaceOnboardingService = betPackMarketPlaceOnboardingService;
  }

  @GetMapping("{brand}/bet-pack/onboarding")
  public ResponseEntity<BetPackOnboarding> getBetPackOnboardingByBrand(@PathVariable String brand) {
    List<BetPackOnboarding> betPackBannerByBrand =
        betPackMarketPlaceOnboardingService.getBpmpOnboardingByBrand(brand);
    if (!betPackBannerByBrand.isEmpty()) {
      BetPackOnboarding betPackOnboarding = betPackBannerByBrand.get(0);
      return new ResponseEntity<>(betPackOnboarding, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
  }
}
