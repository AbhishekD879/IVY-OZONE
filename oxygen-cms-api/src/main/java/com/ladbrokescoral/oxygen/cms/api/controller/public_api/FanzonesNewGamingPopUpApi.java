package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesNewGamingPopUpService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FanzonesNewGamingPopUpApi implements Public {

  private FanzonesNewGamingPopUpService fanzonesNewGamingPopUpService;

  @Autowired
  public FanzonesNewGamingPopUpApi(FanzonesNewGamingPopUpService fanzonesNewGamingPopUpService) {
    this.fanzonesNewGamingPopUpService = fanzonesNewGamingPopUpService;
  }

  @GetMapping("{brand}/fanzone-new-gaming-pop-up")
  public Optional<FanzoneNewGamingPopUp> getFanzoneNewGamingPopup(@PathVariable String brand) {
    return fanzonesNewGamingPopUpService.findAllByBrand(brand);
  }
}
