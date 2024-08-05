package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BybLeaguePublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BybLeagueApi implements Public {

  private final BybLeaguePublicService service;

  @Autowired
  public BybLeagueApi(BybLeaguePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/byb-leagues")
  public List<BybLeagueDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }
}
