package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicSplashPageDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideSplashPagePublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FreeRideSplashPageApi implements Public {

  private final FreeRideSplashPagePublicService service;

  public FreeRideSplashPageApi(FreeRideSplashPagePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/freeride-splashpage")
  public List<FreeRidePublicSplashPageDto> freeRideSplashPageByBrand(
      @PathVariable("brand") String brand) {
    return service.getFreeRideSplashPageByBrand(brand);
  }
}
