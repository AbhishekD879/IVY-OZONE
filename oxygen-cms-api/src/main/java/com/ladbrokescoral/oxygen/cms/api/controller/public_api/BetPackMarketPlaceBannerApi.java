package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicBannerService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BetPackMarketPlaceBannerApi implements Public {

  private BetPackMarketPlacePublicBannerService betPackMarketPlacePublicBannerService;

  public BetPackMarketPlaceBannerApi(
      BetPackMarketPlacePublicBannerService betPackMarketPlacePublicBannerService) {
    this.betPackMarketPlacePublicBannerService = betPackMarketPlacePublicBannerService;
  }

  @GetMapping("{brand}/bet-pack/banner")
  public ResponseEntity<BetPackBanner> getBetPackByBrand(@PathVariable String brand) {
    List<BetPackBanner> betPackBannerByBrand =
        betPackMarketPlacePublicBannerService.getBetPackBannerByBrand(brand);
    if (!betPackBannerByBrand.isEmpty()) {
      BetPackBanner banner = betPackBannerByBrand.get(0);
      return new ResponseEntity<>(banner, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
  }
}
