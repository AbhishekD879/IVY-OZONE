package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class BetPackLabelToolTip extends SortableEntity {
  @NotBlank private String reviewErrorTitle;
  @NotBlank private String reviewErrorMessage;
  @NotBlank private String reviewGoToBettingLabel;
  @NotBlank private String reviewGoBettingURL;
  @NotBlank private String betPackInfoLabel;
  @NotBlank private String lessInfoLabel;
  @NotBlank private String betPackSuccessMessage;
  @NotBlank private String featuredBetPackBackgroundLabel;

  @NotBlank private String maxPurchasedTooltip;
  @NotBlank private String limitedTooltip;
  @NotBlank private String soldOutTooltip;
  @NotBlank private String endingSoonTooltip;
  @NotBlank private String expiresInTooltip;
  @NotBlank private String endedTooltip;
  @NotBlank private String maxOnePurchasedTooltip;
  @NotBlank private String serviceError;
}
