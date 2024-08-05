package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class BetSharingUrls extends AbstractEntity {
  private String horseRacingUrl;
  private String footBallUrl;
  private String url5ASide;
  @NotNull private String brandLogoUrl;
  @NotNull private String settledBetsGenericUrl;
  @NotNull private String openBetsGenericUrl;
  @NotNull private String extensionUrl;
  @NotNull private String beGambleAwareLogoUrl;
  @NotNull private String popUpDesc;

  @NotNull private String genericSharingLink;
}
