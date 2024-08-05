package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class UserMenuDto {
  private String svg;
  private String svgId;
  private String targetUri;
  private String linkTitle;
  private String uriMedium;
  private String uriSmall;
  private Boolean activeIfLogout;
  private String qa;
  private Boolean disabled;
  private String showUserMenu;
}
