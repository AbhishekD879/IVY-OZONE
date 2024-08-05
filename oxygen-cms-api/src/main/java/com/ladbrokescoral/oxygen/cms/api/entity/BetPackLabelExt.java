package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class BetPackLabelExt extends BetPackLabelToolTip {
  @NotBlank private String useByLabel;
  @NotBlank private String betPackReview;
  @NotBlank private String maxPurchasedLabel;
  @NotBlank private String limitedLabel;
  @NotBlank private String soldOutLabel;
  @NotBlank private String endingSoonLabel;
  @NotBlank private String expiresInLabel;
  @NotBlank private String endedLabel;
  @NotBlank private String maxOnePurchasedLabel;
  @NotBlank private String goToReviewText;
  @NotBlank private String goToBetbundleText;

  private Filename backgroundImage;
  private String backgroundImageFileName;
}
