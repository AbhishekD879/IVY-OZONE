package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybMarketDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybMarketPublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BybMarketApi implements Public {

  private final BybMarketPublicService service;

  public BybMarketApi(BybMarketPublicService service) {
    this.service = service;
  }

  @GetMapping("{brand}/byb-markets")
  public List<BybMarketDto> findByBrand(@PathVariable String brand) {
    return service.findByBrand(brand);
  }
}
