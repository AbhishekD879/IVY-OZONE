package com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class CouponAndMarketSwitcherDto extends OnboardingDto {
  private String imageUrl;
  private String buttonText;
  private String fileName;
}
