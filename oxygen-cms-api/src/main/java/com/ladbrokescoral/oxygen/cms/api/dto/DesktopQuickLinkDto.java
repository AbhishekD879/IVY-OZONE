package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class DesktopQuickLinkDto {
  private String title;
  private String target;
  private String uriMedium;
  private String uriLarge;
  private Boolean isAtoZQuickLink;
}
