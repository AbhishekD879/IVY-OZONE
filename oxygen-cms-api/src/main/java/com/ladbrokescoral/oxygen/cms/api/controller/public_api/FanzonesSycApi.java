package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesSycService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class FanzonesSycApi implements Public {

  private FanzonesSycService fanzonesSycService;

  @Autowired
  public FanzonesSycApi(FanzonesSycService fanzonesSycService) {
    this.fanzonesSycService = fanzonesSycService;
  }

  /**
   * This API call is used to get FanzoneSyc
   *
   * @param brand
   * @param pageName
   * @return it will return the requested FanzoneSyc
   */
  @GetMapping("{brand}/{pageName}")
  public Optional<FanzoneSyc> findAllByBrandPageName(
      @PathVariable String brand, @PathVariable String pageName) {
    return fanzonesSycService.findAllByBrandAndPageName(brand, pageName);
  }
}
