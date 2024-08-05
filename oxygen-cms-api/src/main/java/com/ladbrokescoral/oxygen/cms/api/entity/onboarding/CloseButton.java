package com.ladbrokescoral.oxygen.cms.api.entity.onboarding;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class CloseButton {
  @NotBlank private String title;
  @NotBlank private String description;
  @NotBlank private String leftButtonDesc;
  @NotBlank private String rightButtonDesc;
}
