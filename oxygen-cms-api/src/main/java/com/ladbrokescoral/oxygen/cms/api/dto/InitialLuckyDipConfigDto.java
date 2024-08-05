package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class InitialLuckyDipConfigDto {
  private Boolean status = Boolean.FALSE;
  private String luckyDipConfigLevel;
  private String luckyDipConfigLevelId;
  private Boolean displayOnCompetitions = Boolean.FALSE;
}
