package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipBannerConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipFieldsConfigV2;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class LuckyDipV2ConfigurationPublicDto {
  private String id;

  private Boolean status = false;

  private String description;
  private String quickStakes;
  private Boolean displayOnCompetitions;

  private String luckyDipConfigLevel;
  private String luckyDipConfigLevelId;

  private LuckyDipBannerConfig luckyDipBannerConfig;

  private LuckyDipFieldsConfigV2 luckyDipFieldsConfig;

  private String playerPageBoxImgPath;
}
