package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.RenderConfigDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RenderConfigPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RenderConfigApi implements Public {

  private final RenderConfigPublicService service;

  @Autowired
  public RenderConfigApi(RenderConfigPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/render-config")
  public List<RenderConfigDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }
}
