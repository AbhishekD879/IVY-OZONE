package com.ladbrokescoral.oxygen.questionengine.model.cms;

import lombok.Data;

@Data
public class EndPage {
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
  private boolean showPrizes;
  private boolean showResults;
  private boolean showAnswersSummary;
  private String successMessage;
  private String errorMessage;
  private String redirectionButtonLabel;
  private String redirectionButtonUrl;
  private String bannerSiteCoreId;
}
