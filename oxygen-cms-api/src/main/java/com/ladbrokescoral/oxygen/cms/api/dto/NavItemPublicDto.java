package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class NavItemPublicDto {
  private String name;
  private String navType;
  private String url;
  private String descriptionTxt;
  private String leaderboardId;
}
