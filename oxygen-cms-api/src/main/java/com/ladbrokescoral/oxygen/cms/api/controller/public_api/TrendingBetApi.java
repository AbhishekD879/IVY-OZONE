package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.TrendingBetService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TrendingBetApi implements Public {
  private final TrendingBetService trendingBetService;

  public TrendingBetApi(TrendingBetService trendingBetService) {
    this.trendingBetService = trendingBetService;
  }

  @GetMapping("{brand}/trending-bet/{type}")
  public TrendingBet getTrendingBetSlipByBrand(
      @PathVariable String brand, @PathVariable String type) {
    return trendingBetService
        .getTrendingBetsByBrand(brand, type)
        .orElseThrow(NotFoundException::new);
  }
}
