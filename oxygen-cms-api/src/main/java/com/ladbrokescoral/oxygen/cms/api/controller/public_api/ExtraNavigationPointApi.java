package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ExtraNavigationPointPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ExtraNavigationPointPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExtraNavigationPointApi implements Public {
  private final ExtraNavigationPointPublicService extraNavigationPointPublicService;

  @Autowired
  public ExtraNavigationPointApi(
      ExtraNavigationPointPublicService extraNavigationPointPublicService) {
    this.extraNavigationPointPublicService = extraNavigationPointPublicService;
  }

  @GetMapping("{brand}/extra-navigation-points")
  public List<ExtraNavigationPointPublicDto> findByBrand(@PathVariable("brand") String brand) {
    return extraNavigationPointPublicService.findAllActiveExtraNavPointsByBrand(brand);
  }
}
