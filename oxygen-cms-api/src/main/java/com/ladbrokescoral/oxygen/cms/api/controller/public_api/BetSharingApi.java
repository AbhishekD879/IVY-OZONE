package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetSharingEntity;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.BetSharingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BetSharingApi implements Public {
  private final BetSharingService betSharingService;

  public BetSharingApi(BetSharingService betSharingService) {
    this.betSharingService = betSharingService;
  }

  @GetMapping("{brand}/bet-sharing")
  public BetSharingEntity getBetSharingByBrand(@PathVariable String brand) {
    return betSharingService.getBetSharingByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
