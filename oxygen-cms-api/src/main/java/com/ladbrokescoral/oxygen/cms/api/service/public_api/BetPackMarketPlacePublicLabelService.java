package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceLabelService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class BetPackMarketPlacePublicLabelService {

  private BetPackMarketPlaceLabelService betPackMarketPlaceLabelService;

  public BetPackMarketPlacePublicLabelService(
      BetPackMarketPlaceLabelService betPackMarketPlaceLabelService) {
    this.betPackMarketPlaceLabelService = betPackMarketPlaceLabelService;
  }

  public List<BetPackLabel> getAllBetPackLabel() {
    return betPackMarketPlaceLabelService.findAll();
  }

  public List<BetPackLabel> getBetPackLabelByBrand(String brand) {
    return betPackMarketPlaceLabelService.findByBrand(brand);
  }
}
