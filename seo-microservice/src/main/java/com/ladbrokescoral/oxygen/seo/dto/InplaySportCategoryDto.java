package com.ladbrokescoral.oxygen.seo.dto;

import lombok.Data;

@Data
public class InplaySportCategoryDto {
  private String alt;
  private String imageTitle;
  private String categoryPath;
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

  private String svgId;
}
