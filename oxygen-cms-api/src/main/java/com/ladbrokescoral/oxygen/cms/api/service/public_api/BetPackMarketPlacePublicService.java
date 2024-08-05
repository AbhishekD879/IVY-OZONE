package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class BetPackMarketPlacePublicService {

  private final BetPackMarketPlaceService betPackMarketPlaceService;

  public BetPackMarketPlacePublicService(BetPackMarketPlaceService betPackMarketPlaceService) {
    this.betPackMarketPlaceService = betPackMarketPlaceService;
  }

  public List<BetPackEntity> getAllBetPack() {
    return betPackMarketPlaceService.findAll();
  }

  public List<BetPackEntity> getActiveBetPackByBrand(String brand) {
    return betPackMarketPlaceService.findAllActiveBetPackEntities(brand);
  }

  public List<String> getActiveBetPackId(String brand) {
    return betPackMarketPlaceService.getActiveBetPackId(brand);
  }

  public List<BetPackEntity> findAllBetPacksBetweenDate(String brand) {
    return betPackMarketPlaceService.findAllBetPacksBetweenDate(brand);
  }
}
