package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class NavigationGroupPublicService {
  private final NavItemPublicService navItemPublicService;

  public NavigationGroupPublicService(NavItemPublicService navItemPublicService) {
    this.navItemPublicService = navItemPublicService;
  }

  public List<NavigationGroupPublicDto> getNavigationGroupByBrand(String brand) {
    return navItemPublicService.getNavigationGroupByBrand(brand);
  }
}
