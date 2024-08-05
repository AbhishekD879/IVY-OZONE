package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingPublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LuckyDipMappingApi implements Public {

  private final LuckyDipMappingPublicService service;

  public LuckyDipMappingApi(LuckyDipMappingPublicService service) {
    this.service = service;
  }

  @GetMapping("{brand}/lucky-dip-mapping")
  public List<LuckyDipMappingPublicDto> getAllActiveLuckyDipMappingsByBrand(
      @PathVariable("brand") String brand) {
    return service.findAllActiveLuckyDipMappingsByBrand(brand);
  }
}
