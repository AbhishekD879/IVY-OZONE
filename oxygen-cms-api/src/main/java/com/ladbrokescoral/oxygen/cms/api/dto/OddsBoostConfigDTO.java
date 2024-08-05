package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
public class OddsBoostConfigDTO {
  private boolean enabled = false;
  private String loggedOutHeaderText;
  private String loggedInHeaderText;
  private String termsAndConditionsText;
  private String moreLink;
  private String svg;
  private String svgId;
  private String svgFilename;
  private String lang;
  private boolean allowUserToToggleVisibility;
  private int daysToKeepPopupHidden;
  private String countDownTimer;
  private String noTokensText;
}
