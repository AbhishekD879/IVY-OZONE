package com.ladbrokescoral.oxygen.cms.api.entity.onboarding;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class OnBoarding extends AbstractEntity implements HasBrand {

  @Brand private String brand;
  private Boolean isEnable;
  private String imageUrl;
  private Integer heightMedium;
  private Integer widthMedium;
  private String fileName;
  private Boolean expiryDateEnabled;
}
