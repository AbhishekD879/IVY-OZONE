package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.LeagueLinkService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class LeagueLinkApi implements Public {
  private final LeagueLinkService service;

  @JsonView(Views.Public.class)
  @GetMapping("{brand}/league-links/{couponId}")
  public List<LeagueLink> getLeagueLinksByCouponId(
      @PathVariable("brand") String brand, @PathVariable int couponId) {
    return service.getEnabledLeagueLinksByCouponId(brand, couponId);
  }
}
