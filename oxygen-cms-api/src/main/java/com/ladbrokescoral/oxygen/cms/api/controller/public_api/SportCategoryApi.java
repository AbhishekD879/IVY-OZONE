package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryNativeDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportCategoryPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SportCategoryApi implements Public {

  private final SportCategoryPublicService service;

  @Autowired
  public SportCategoryApi(SportCategoryPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/sport-category")
  public List<SportCategoryDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }

  @GetMapping(value = "{brand}/sport-category-native")
  public List<SportCategoryNativeDto> findByBrandCategoryNative(
      @PathVariable("brand") String brand) {
    return service.findNative(brand);
  }
}
