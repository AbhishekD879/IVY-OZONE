package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneOptinEmail;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesOptinEmailService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class FanzoneOptinEmailApi implements Public {

  private FanzonesOptinEmailService fanzonesOptinEmailService;

  @Autowired
  public FanzoneOptinEmailApi(FanzonesOptinEmailService fanzonesOptinEmailService) {
    this.fanzonesOptinEmailService = fanzonesOptinEmailService;
  }

  /* Method description
  @brand represent brand name
  @pagename represent the entity name
  @return it will return all the requested SpecialPages.
   */
  @GetMapping("{brand}/fanzones/fanzone-optin-email")
  public Optional<FanzoneOptinEmail> findAllByBrand(@PathVariable String brand) {
    return fanzonesOptinEmailService.findFanzoneOptinEmailByBrand(brand);
  }
}
