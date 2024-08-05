package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class SeasonTeam {
  @NotBlank private String assetManagementObjectId;
}
