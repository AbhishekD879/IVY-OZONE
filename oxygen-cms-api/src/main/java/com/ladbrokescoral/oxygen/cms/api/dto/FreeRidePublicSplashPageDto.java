package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class FreeRidePublicSplashPageDto {

  private String id;
  private String brand;
  private String welcomeMsg;
  private String termsAndCondition;
  private String termsAndConditionLink;
  private String termsAndConditionHyperLinkText;
  private String buttonText;
  private String splashImageUrl;
  private String bannerImageUrl;
  private String freeRideLogoUrl;

  private Boolean isHomePage;
  private Boolean isBetReceipt;
  private String promoUrl;
}
