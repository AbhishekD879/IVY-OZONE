package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.YcStaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.YourCallStaticBlockPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class YourCallStaticBlockApi implements Public {

  private final YourCallStaticBlockPublicService service;

  @Autowired
  public YourCallStaticBlockApi(YourCallStaticBlockPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/yc-static-block")
  public List<YcStaticBlockDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }

  @GetMapping(value = "{brand}/5a-side-static-block")
  public List<YcStaticBlockDto> find5AByBrand(@PathVariable("brand") String brand) {
    return service.findByBrandAnd5A(brand);
  }
}
