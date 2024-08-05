package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CountrySettingDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CountryPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CountryApi implements Public {

  private final CountryPublicService service;

  @Autowired
  public CountryApi(CountryPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/countries-settings")
  public List<CountrySettingDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand);
  }
}
