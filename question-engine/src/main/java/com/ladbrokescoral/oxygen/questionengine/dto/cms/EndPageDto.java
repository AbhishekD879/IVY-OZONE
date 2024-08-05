package com.ladbrokescoral.oxygen.questionengine.dto.cms;

import lombok.Data;

@Data
public class EndPageDto {
  private String title;

  private String backgroundSvgImagePath;

  private String gameDescription;
  private String submitMessage;
  private String upsellBetInPlayCtaText;
  private String noPreviousRoundMessage;
  private String noLatestRoundMessage;
  private String upsellAddToBetslipCtaText;
  private String submitCta;

  private boolean showUpsell;
  private boolean showAnswersSummary;
  private boolean showResults;
  private boolean showPrizes;
  private String successMessage;
  private String errorMessage;
  private String redirectionButtonLabel;
  private String redirectionButtonUrl;
  private String bannerSiteCoreId;
}
