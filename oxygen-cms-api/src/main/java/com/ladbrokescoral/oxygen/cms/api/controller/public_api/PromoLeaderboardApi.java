package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoLeaderboardConfigPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.PromoLeaderboardPublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PromoLeaderboardApi implements Public {
  private PromoLeaderboardPublicService promoLeaderboardPublicService;

  public PromoLeaderboardApi(PromoLeaderboardPublicService promoLeaderboardPublicService) {
    this.promoLeaderboardPublicService = promoLeaderboardPublicService;
  }

  @GetMapping("{brand}/promo-leaderboard")
  public List<PromoLeaderboardConfigPublicDto> findPromoLeaderboardByBrand(
      @PathVariable("brand") String brand) {
    return promoLeaderboardPublicService.findLeaderboardByBrand(brand);
  }
}
