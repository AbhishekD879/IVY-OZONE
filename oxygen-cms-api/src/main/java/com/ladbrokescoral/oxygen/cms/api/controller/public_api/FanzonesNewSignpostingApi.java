package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewSignpostingService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FanzonesNewSignpostingApi implements Public {

  private FanzonesNewSignpostingService fanzonesNewSignpostingService;

  @Autowired
  public FanzonesNewSignpostingApi(FanzonesNewSignpostingService fanzonesNewSignpostingService) {
    this.fanzonesNewSignpostingService = fanzonesNewSignpostingService;
  }

  @GetMapping("{brand}/fanzone-new-signposting")
  public Optional<FanzoneNewSignposting> findAllByBrand(@PathVariable String brand) {
    return fanzonesNewSignpostingService.findAllByBrand(brand);
  }
}
