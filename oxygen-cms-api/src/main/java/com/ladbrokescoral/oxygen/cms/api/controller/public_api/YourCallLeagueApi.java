package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.YcLeagueDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.YourCallLeaguePublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class YourCallLeagueApi implements Public {

  private final YourCallLeaguePublicService service;

  @Autowired
  public YourCallLeagueApi(YourCallLeaguePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/yc-leagues")
  public List<YcLeagueDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }
}
