package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class FooterMenuIntermediateContainerDto {

  private Integer mobile = 0;
  private Integer tablet = 0;
  private Integer desktop = 0;
  private List<FooterMenu> footerMenus = new ArrayList<>();
}
