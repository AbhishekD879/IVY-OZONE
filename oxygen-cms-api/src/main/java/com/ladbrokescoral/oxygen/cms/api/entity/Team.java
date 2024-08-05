package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class Team {

  @NotBlank private String name;

  @NotBlank private String displayName;

  @NotBlank private String teamKitIcon;

  private Boolean isNonPLTeam; // true - Don't allocate the badge and no validation required
}
