package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class LuckyDipFieldsConfigV2 {
  @NotBlank private String title;
  @NotBlank private String welcomeMessage;
  @NotBlank private String betPlacementTitle;
  @NotBlank private String betPlacementStep1;
  @NotBlank private String betPlacementStep2;
  @NotBlank private String betPlacementStep3;
  @NotBlank private String termsAndConditionsURL;
  @NotBlank private String playerCardDesc;
  @NotBlank private String potentialReturnsDesc;
  @NotBlank private String placebetCTAButton;
  @NotBlank private String backCTAButton;
  @NotBlank private String gotItCTAButton;
  @NotBlank private String depositButton;
}
