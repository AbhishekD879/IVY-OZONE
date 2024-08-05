package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipBannerConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipFieldsConfig;
import lombok.Data;

@Data
public class LuckyDipConfigurationPublicDto {
  private String id;

  private LuckyDipBannerConfig luckyDipBannerConfig;

  private LuckyDipFieldsConfig luckyDipFieldsConfig;

  private String playerPageBoxImgPath;
}
