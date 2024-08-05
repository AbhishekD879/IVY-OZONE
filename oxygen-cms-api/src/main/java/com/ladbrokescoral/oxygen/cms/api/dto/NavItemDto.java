package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class NavItemDto {
  private String id;
  private String brand;
  private String name;
  private String navigationGroupId;
  private String navType;
  private String url;
  private String descriptionTxt;
  private String leaderboardId;
  private Boolean leaderboardStatus;
}
