package com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding;

import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class CouponStatsWidgetDto extends OnboardingDto {

  @NotBlank private String buttonText;
  private Instant displayFrom;
  private Instant displayTo;
}
