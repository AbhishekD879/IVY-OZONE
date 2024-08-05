package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SportPageConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportTabConfigListDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import java.util.List;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
public class SportConfigApi implements Public {

  private final SportCategoryPublicService service;

  @GetMapping("/{brand}/sport-tabs/{categoryId}")
  public SportTabConfigListDto getSportTabs(
      @PathVariable String brand, @PathVariable Integer categoryId) {
    return service.getSportTabs(brand, categoryId);
  }

  /** @deprecated delete when /sport-tabs will be on Live for both brands */
  @Deprecated
  @GetMapping("/{brand}/sport-config/{categoryId}")
  public SportPageConfigDto getSportConfig(
      @PathVariable String brand, @PathVariable Integer categoryId) {
    return service.getSportConfig(brand, categoryId);
  }

  /** @deprecated delete when /sport-tabs will be on Live for both brands */
  @Deprecated
  @GetMapping("/{brand}/sport-config")
  public List<SportPageConfigDto> getSportsConfigs(
      @PathVariable String brand, @RequestParam List<Integer> categoryIds) {
    return service.getSportsConfigs(brand, categoryIds);
  }
}
