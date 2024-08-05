package com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class StepContentDto {

  @NotBlank private String title;
  @NotBlank private String description;
}
