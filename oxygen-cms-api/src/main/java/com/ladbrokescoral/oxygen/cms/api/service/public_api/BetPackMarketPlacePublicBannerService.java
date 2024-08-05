package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceBannerService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class BetPackMarketPlacePublicBannerService {

  private BetPackMarketPlaceBannerService betPackMarketPlaceBannerService;

  public BetPackMarketPlacePublicBannerService(
      BetPackMarketPlaceBannerService betPackMarketPlaceBannerService) {
    this.betPackMarketPlaceBannerService = betPackMarketPlaceBannerService;
  }

  public List<BetPackBanner> getBetPackBannerByBrand(String brand) {
    return betPackMarketPlaceBannerService.findByBrand(brand);
  }
}
