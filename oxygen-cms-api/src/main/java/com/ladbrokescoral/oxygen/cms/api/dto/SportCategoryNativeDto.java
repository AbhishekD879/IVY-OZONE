package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SportCategoryNativeDto extends BaseUIDto {
  private String alt;
  private String imageTitle;
  private Integer categoryId;
  private String ssCategoryCode;
  private String targetUri;
  private boolean disabled;
  private boolean showInPlay;
  private boolean showInHome;
  private boolean showInAZ;
  private String path;
  private Boolean isTopSport;
  private boolean inApp;
  private boolean showScoreboard;
  private String scoreBoardUrl;
  private boolean hasEvents;
  private boolean inplayEnabled;
  // OZONE-3426 added this field for non runner horse message for extrasignplace posting
  private String messageLabel;

  private boolean isReactionsEnabled;

  @JsonProperty("isReactionsEnabled")
  public boolean isReactionsEnabled() {
    return isReactionsEnabled;
  }
}
