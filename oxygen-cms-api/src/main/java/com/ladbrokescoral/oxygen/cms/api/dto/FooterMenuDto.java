package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class FooterMenuDto extends BaseMenuDto {
  private String svg;
  private String svgId;
  private String uriSmall;
  private String showItemFor;
  private String spriteClass;
}
