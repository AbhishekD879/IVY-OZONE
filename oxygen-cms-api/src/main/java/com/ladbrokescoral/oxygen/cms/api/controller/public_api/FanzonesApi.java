package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Fanzone;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class FanzonesApi implements Public {

  private FanzonesService fanzonesService;

  @Autowired
  public FanzonesApi(FanzonesService fanzonesService) {
    this.fanzonesService = fanzonesService;
  }

  /* Method description
  @brand represent brand name
  @pagename represent the entity name
  @return it will return all the requested SpecialPages.
   */
  @GetMapping("{brand}/fanzone")
  public Optional<List<Fanzone>> findAllByPageName(@PathVariable String brand) {
    return fanzonesService.findAllFanzonesByBrand(brand);
  }
}
