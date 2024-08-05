package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfGameTabsDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OtfGameTabPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class OtfGameTabsApi implements Public {
  private final OtfGameTabPublicService otfGameTabPublicService;

  @GetMapping("{brand}/one-two-free/otf-tab-config")
  public List<OtfGameTabsDto> findOtfGameTabByBrand(@PathVariable("brand") String brand) {
    return otfGameTabPublicService.findByBrand(brand);
  }
}
