package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesComingBackService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FanzonesComingBackApiController implements Public {

  private FanzonesComingBackService fanzonesComingBackService;

  @Autowired
  public FanzonesComingBackApiController(FanzonesComingBackService fanzonesComingBackService) {
    this.fanzonesComingBackService = fanzonesComingBackService;
  }

  @GetMapping("{brand}/fanzone-coming-back")
  public Optional<FanzoneComingBack> findAllByBrand(@PathVariable String brand) {
    return fanzonesComingBackService.findAllByBrand(brand);
  }
}
