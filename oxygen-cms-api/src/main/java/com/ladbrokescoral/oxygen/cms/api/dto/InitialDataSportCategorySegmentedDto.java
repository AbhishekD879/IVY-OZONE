package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class InitialDataSportCategorySegmentedDto extends AbstractSegmentDto {

  private String id;
  private String alt;
  private String imageTitle;
  private String ssCategoryCode;
  private String targetUri;
  private String path;
  private String svg;
  private String svgId;
  private String scoreBoardUrl;
  private boolean disabled;
  private boolean showInPlay;
  private boolean showInHome;
  private boolean showInAZ;
  private boolean inApp;
  private boolean showScoreboard;
  private boolean hasEvents;
  private Boolean isTopSport;
  private Integer categoryId;
  private Double sortOrder;
  private InitialSportPageConfigDto sportConfig;
  private InplayStatsConfigDto inplayStatsConfigDto;
  private boolean showFreeRideBanner;
}
