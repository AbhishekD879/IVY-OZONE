package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipBannerConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipFieldsConfigV2;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import lombok.Data;

@Data
public class LuckyDipV2ConfigurationDto {
  private String id;

  @Brand private String brand;

  private Boolean status = false;

  private String description;
  private String quickStakes;
  private Boolean displayOnCompetitions;

  private String luckyDipConfigLevel;
  private String luckyDipConfigLevelId;

  private LuckyDipBannerConfig luckyDipBannerConfig;

  @Valid private LuckyDipFieldsConfigV2 luckyDipFieldsConfig;

  private String playerPageBoxImgPath;
}
