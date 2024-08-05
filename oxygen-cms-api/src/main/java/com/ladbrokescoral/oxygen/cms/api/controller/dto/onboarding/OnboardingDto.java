package com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.AbstractDto;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class OnboardingDto extends AbstractDto {

  private String brand;
  private Boolean isEnable;
  private Integer heightMedium;
  private Integer widthMedium;
  private String fileName;
  private String imageUrl;
  private Boolean expiryDateEnabled;
}
