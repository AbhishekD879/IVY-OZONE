package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackEnablerFilterService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class BetPackMarketPlacePublicFilterService {

  private BetPackEnablerFilterService betPackEnablerFilterService;

  public BetPackMarketPlacePublicFilterService(
      BetPackEnablerFilterService betPackEnablerFilterService) {
    this.betPackEnablerFilterService = betPackEnablerFilterService;
  }

  public List<BetPackFilter> getAllBetPackFilter() {
    return betPackEnablerFilterService.findAll();
  }

  public List<BetPackFilter> getActiveBetPackFilterByBrand(String brand) {
    return betPackEnablerFilterService.findAllActiveBetPackFilter(brand);
  }
}
