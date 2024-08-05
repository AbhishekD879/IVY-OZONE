package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackLabel;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicLabelService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BetPackMarketPlaceLabelApi implements Public {

  private BetPackMarketPlacePublicLabelService betPackMarketPlacePublicLabelService;

  public BetPackMarketPlaceLabelApi(
      BetPackMarketPlacePublicLabelService betPackMarketPlacePublicLabelService) {
    this.betPackMarketPlacePublicLabelService = betPackMarketPlacePublicLabelService;
  }

  @GetMapping("bet-pack/labels")
  public List<BetPackLabel> getAllBetPack() {
    return betPackMarketPlacePublicLabelService.getAllBetPackLabel();
  }

  @GetMapping("{brand}/bet-pack/label")
  public ResponseEntity<BetPackLabel> getBetPackByBrand(@PathVariable String brand) {
    List<BetPackLabel> betPackLabelByBrand =
        betPackMarketPlacePublicLabelService.getBetPackLabelByBrand(brand);
    if (!betPackLabelByBrand.isEmpty()) {
      BetPackLabel label = betPackLabelByBrand.get(0);
      return new ResponseEntity<>(label, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
  }
}
