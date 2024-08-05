package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class NavigationGroupPublicDto {
  private String id;
  private String brand;
  private String title;
  private Boolean status;
  private List<NavItemPublicDto> navItems;
}
