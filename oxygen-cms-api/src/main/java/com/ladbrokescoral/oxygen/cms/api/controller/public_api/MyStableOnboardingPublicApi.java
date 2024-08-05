package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.MyStableOnboarding;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.MyStableOnboardingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyStableOnboardingPublicApi implements Public {
  private final MyStableOnboardingService myStableOnboardingService;

  public MyStableOnboardingPublicApi(MyStableOnboardingService myStableOnboardingService) {
    this.myStableOnboardingService = myStableOnboardingService;
  }

  @GetMapping("/{brand}/my-stable/onboarding")
  public MyStableOnboarding findByBrand(@PathVariable String brand) {

    return myStableOnboardingService.readByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
