package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "luckydipconfig")
public class LuckyDipConfiguration extends AbstractEntity implements HasBrand {
  @Brand private String brand;

  private LuckyDipBannerConfig luckyDipBannerConfig;

  @Valid private LuckyDipFieldsConfig luckyDipFieldsConfig;

  private String playerPageBoxImgPath;
}
