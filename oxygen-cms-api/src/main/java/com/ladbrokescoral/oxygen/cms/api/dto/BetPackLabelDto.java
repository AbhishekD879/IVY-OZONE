package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.AccessLevel;
import lombok.Data;
import lombok.Getter;

@Data
public class BetPackLabelDto {
  private String id;
  @NotBlank private String brand;
  @NotBlank private String buyButtonLabel;
  @NotBlank private String buyBetPackLabel;
  @NotBlank private String gotoMyBetPacksLabel;
  @NotBlank private String depositMessage;
  @NotBlank private String maxBetPackPerDayBannerLabel;
  @NotBlank private String betPackAlreadyPurchasedPerDayBannerLabel;
  @NotBlank private String betPackMarketplacePageTitle;
  @NotBlank private String errorTitle;
  @NotBlank private String errorMessage;
  @NotBlank private String goToBettingLabel;
  @NotBlank private String goBettingURL;
  @NotBlank private String moreInfoLabel;
  @NotBlank private String buyNowLabel;
  @NotBlank private String kycArcGenericMessage;
  @NotBlank private String useByLabel;
  @NotBlank private String betPackReview;
  @NotBlank private String maxPurchasedLabel;
  @NotBlank private String limitedLabel;
  @NotBlank private String soldOutLabel;
  @NotBlank private String endingSoonLabel;
  @NotBlank private String expiresInLabel;
  @NotBlank private String endedLabel;
  @NotBlank private String maxOnePurchasedLabel;

  @NotBlank private String reviewErrorTitle;
  @NotBlank private String reviewErrorMessage;
  @NotBlank private String reviewGoToBettingLabel;
  @NotBlank private String reviewGoBettingURL;
  @NotBlank private String betPackInfoLabel;
  @NotBlank private String lessInfoLabel;
  @NotBlank private String betPackSuccessMessage;
  @NotBlank private String featuredBetPackBackgroundLabel;

  private Filename backgroundImage;
  private String backgroundImageFileName;

  @NotBlank private String maxPurchasedTooltip;
  @NotBlank private String limitedTooltip;
  @NotBlank private String soldOutTooltip;
  @NotBlank private String endingSoonTooltip;
  @NotBlank private String expiresInTooltip;
  @NotBlank private String endedTooltip;
  @NotBlank private String maxOnePurchasedTooltip;
  @NotBlank private String serviceError;
  @NotBlank private String goToReviewText;
  @NotBlank private String goToBetbundleText;

  private boolean isAllFilterPillMessageActive;
  private String allFilterPillMessage;

  @Getter(AccessLevel.NONE)
  @NotNull
  private boolean isDailyLimitBannerEnabled;

  @JsonProperty("isDailyLimitBannerEnabled")
  public boolean isDailyLimitBannerEnabled() {
    return isDailyLimitBannerEnabled;
  }

  @NotBlank private String comingSoon;
  private String comingSoonSvg;
}
