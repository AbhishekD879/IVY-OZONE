package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class SportsRibbonItem {

  private Integer categoryId;
  private String categoryName;
  private String categoryCode;
  private Integer displayOrder;
  private Boolean hasLiveNow = false;
  private Boolean hasUpcoming = false;
  private Boolean hasLiveStream = false;
  private Boolean hasUpcommingLiveStream = false;
  private String alt;
  private String defaultTab;
  private Boolean disabled;
  private List<String> dispSortName;

  @JsonProperty("filename")
  private String fileName;

  private Integer heightMedium;
  private Integer heightSmall;
  private String imageTitle;
  private Boolean inApp;
  private Boolean isMultiTemplateSport;
  private Boolean isOutrightSport;
  private Map<String, String> oddsCardHeaderType;
  private String primaryMarkets;
  private boolean showInPlay;
  private String ssCategoryCode;
  private String svgId;
  private Tab tabs;
  private String targetUri;
  private String targetUriCopy;
  private List<String> typeIds;
  private String uriMedium;
  private String uriMediumIcon;
  private String uriSmall;
  private String uriSmallIcon;
  private List<String> viewByFilters;
  private Integer widthMedium;
  private Integer widthSmall;
  private int liveEventCount;
  private int upcomingEventCount;
  private int liveStreamEventCount;
  private int upcommingLiveStreamEventCount;
}
