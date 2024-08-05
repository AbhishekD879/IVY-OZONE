package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.onboarding.FirstBetPlaceTutorialService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FirstBetPlaceTutorialPublicApi implements Public {

  private final FirstBetPlaceTutorialService firstBetPlaceTutorialService;

  public FirstBetPlaceTutorialPublicApi(FirstBetPlaceTutorialService firstBetPlaceTutorialService) {
    this.firstBetPlaceTutorialService = firstBetPlaceTutorialService;
  }

  @GetMapping("/first-bet-place-tutorial/brand/{brand}")
  public FirstBetPlaceTutorial findByBrand(@PathVariable String brand) {

    return firstBetPlaceTutorialService.readByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
