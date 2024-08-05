package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybWidgetPublicService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BybWidgetApi implements Public {

  private final BybWidgetPublicService service;

  public BybWidgetApi(BybWidgetPublicService service) {
    this.service = service;
  }

  @GetMapping("{brand}/byb-widgets")
  public BybWidgetDto findAllByBrand(@PathVariable @Brand String brand) {

    return service.readByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
