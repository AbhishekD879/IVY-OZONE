package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class TeamDto {
  private String name;
  private String displayName;
  private String teamKitIcon;
  private Boolean isNonPLTeam;
}
