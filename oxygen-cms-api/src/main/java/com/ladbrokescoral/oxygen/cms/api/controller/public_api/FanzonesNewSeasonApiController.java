package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSeasonService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FanzonesNewSeasonApiController implements Public {

  private FanzonesNewSeasonService fanzonesNewSeasonService;

  @Autowired
  public FanzonesNewSeasonApiController(FanzonesNewSeasonService fanzonesNewSeasonService) {
    this.fanzonesNewSeasonService = fanzonesNewSeasonService;
  }

  @GetMapping("{brand}/fanzone-new-season")
  public Optional<FanzoneNewSeason> findAllByBrand(@PathVariable String brand) {
    return fanzonesNewSeasonService.findAllByBrand(brand);
  }
}
