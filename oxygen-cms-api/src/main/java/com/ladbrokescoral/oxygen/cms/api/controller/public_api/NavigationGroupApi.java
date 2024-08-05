package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.NavigationGroupPublicService;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NavigationGroupApi implements Public {

  private NavigationGroupPublicService navigationGroupPublicService;

  public NavigationGroupApi(NavigationGroupPublicService navigationGroupPublicService) {
    this.navigationGroupPublicService = navigationGroupPublicService;
  }

  @GetMapping("{brand}/navigation-group")
  public List<NavigationGroupPublicDto> getNavigationGroupByBrand(
      @PathVariable("brand") String brand) {
    return navigationGroupPublicService.getNavigationGroupByBrand(brand);
  }
}
