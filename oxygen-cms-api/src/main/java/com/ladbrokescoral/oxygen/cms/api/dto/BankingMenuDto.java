package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class BankingMenuDto extends BaseMenuDto {
  private String svg;
  private String svgId;
  private String uriLarge;
  private String uriMedium;
  private String uriSmall;
  private String section;
  private String type;
  private String showItemFor;
  private List<String> showOnlyOnOS;
  private String qa;
  private String iconAlignment;
  private Boolean authRequired;
  private Integer systemID;
  private String buttonClass;
  private String startUrl;
  private String subHeader;
}
