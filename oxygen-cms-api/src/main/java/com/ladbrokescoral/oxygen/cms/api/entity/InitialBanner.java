package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class InitialBanner {
  private String desktopBannerId;

  private String mobileBannerId;

  private String bannerPosition;

  private boolean isBannerEnabled;
  private String ctaButtonLabel;
  private String redirectionUrl;
}
