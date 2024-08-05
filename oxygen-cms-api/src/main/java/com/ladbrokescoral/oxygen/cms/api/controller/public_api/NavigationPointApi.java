package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationPointDto;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationPointServiceCacheable;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NavigationPointApi implements Public {
  private NavigationPointServiceCacheable cacheableNavigationPointService;

  @Autowired
  public NavigationPointApi(NavigationPointServiceCacheable cacheableNavigationPointService) {
    this.cacheableNavigationPointService = cacheableNavigationPointService;
  }

  @GetMapping("{brand}/navigation-points")
  public List<NavigationPointDto> findByBrand(@PathVariable("brand") String brand) {
    return cacheableNavigationPointService.getNavigationPointByBrandEnabled(brand);
  }
}
