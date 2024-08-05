package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicService;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BetPackMarketPlaceApi implements Public {

  private final BetPackMarketPlacePublicService betPackMarketPlacePublicService;

  public BetPackMarketPlaceApi(BetPackMarketPlacePublicService betPackMarketPlacePublicService) {
    this.betPackMarketPlacePublicService = betPackMarketPlacePublicService;
  }

  @GetMapping("bet-packs")
  public List<BetPackEntity> getAllBetPack() {
    return betPackMarketPlacePublicService.getAllBetPack();
  }

  @GetMapping("{brand}/bet-pack")
  public List<BetPackEntity> getBetPackByBrand(@PathVariable String brand) {
    return betPackMarketPlacePublicService.getActiveBetPackByBrand(brand);
  }

  @GetMapping("{brand}/active-bet-pack-ids")
  public List<String> getActiveBetPackIds(@PathVariable String brand) {
    List<String> activeBetPackIds = betPackMarketPlacePublicService.getActiveBetPackId(brand);
    return CollectionUtils.isNotEmpty(activeBetPackIds)
        ? activeBetPackIds.stream().distinct().collect(Collectors.toList())
        : Collections.emptyList();
  }
}
