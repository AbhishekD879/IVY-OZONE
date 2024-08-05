package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.MarketLinkService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class MarketLinkApi implements Public {

  private final MarketLinkService service;

  @JsonView(Views.Public.class)
  @GetMapping("{brand}/market-links")
  public List<MarketLink> getLeagueLinksByCouponId(@PathVariable("brand") String brand) {
    return service.getMarketLinksByBrand(brand);
  }
}
