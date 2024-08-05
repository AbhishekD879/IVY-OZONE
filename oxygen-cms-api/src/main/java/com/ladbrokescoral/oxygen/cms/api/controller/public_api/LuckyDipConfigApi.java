package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipConfigurationPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.LuckyDipConfigPublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LuckyDipConfigApi implements Public {

  private final LuckyDipConfigPublicService service;

  public LuckyDipConfigApi(LuckyDipConfigPublicService service) {
    this.service = service;
  }

  @GetMapping("{brand}/luckydip")
  public List<LuckyDipConfigurationPublicDto> getAllLuckyDipConfigByBrand(
      @PathVariable("brand") String brand) {
    return service.getAllLuckyDipConfigByBrand(brand);
  }
}
