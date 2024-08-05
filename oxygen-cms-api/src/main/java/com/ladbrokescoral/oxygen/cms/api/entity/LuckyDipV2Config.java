package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "lucky-dip-config")
public class LuckyDipV2Config extends AbstractEntity implements HasBrand {
  @Brand private String brand;

  private Boolean status;

  private String description;
  private String quickStakes;
  private Boolean displayOnCompetitions;

  private String luckyDipConfigLevel;

  @Indexed(unique = true)
  @NotNull
  private String luckyDipConfigLevelId;

  private LuckyDipBannerConfig luckyDipBannerConfig;

  @Valid private LuckyDipFieldsConfigV2 luckyDipFieldsConfig;

  private String playerPageBoxImgPath;
}
