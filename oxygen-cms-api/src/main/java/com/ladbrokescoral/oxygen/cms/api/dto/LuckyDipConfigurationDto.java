package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipBannerConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipFieldsConfig;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import lombok.Data;

@Data
public class LuckyDipConfigurationDto {
  private String id;

  @Brand private String brand;

  private LuckyDipBannerConfig luckyDipBannerConfig;

  @Valid private LuckyDipFieldsConfig luckyDipFieldsConfig;

  private String playerPageBoxImgPath;
}
