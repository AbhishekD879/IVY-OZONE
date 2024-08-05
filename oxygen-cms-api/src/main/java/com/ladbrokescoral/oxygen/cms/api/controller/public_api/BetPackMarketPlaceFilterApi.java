package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicFilterService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BetPackMarketPlaceFilterApi implements Public {

  private BetPackMarketPlacePublicFilterService betPackMarketPlacePublicFilterService;

  public BetPackMarketPlaceFilterApi(
      BetPackMarketPlacePublicFilterService betPackMarketPlacePublicFilterService) {
    this.betPackMarketPlacePublicFilterService = betPackMarketPlacePublicFilterService;
  }

  @GetMapping("bet-pack/filters")
  public List<BetPackFilter> getAllBetPack() {
    return betPackMarketPlacePublicFilterService.getAllBetPackFilter();
  }

  @GetMapping("{brand}/bet-pack/filter")
  public List<BetPackFilter> getBetPackByBrand(@PathVariable String brand) {
    return betPackMarketPlacePublicFilterService.getActiveBetPackFilterByBrand(brand);
  }
}
