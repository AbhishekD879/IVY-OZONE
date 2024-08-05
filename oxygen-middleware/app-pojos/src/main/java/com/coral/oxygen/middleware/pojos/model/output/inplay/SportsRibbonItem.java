package com.coral.oxygen.middleware.pojos.model.output.inplay;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.Tab;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.util.List;
import java.util.Map;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;

@Setter
@Accessors(chain = true)
@ToString
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

  @SerializedName("filename")
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

  @ChangeDetect
  public Integer getCategoryId() {
    return categoryId;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  @ChangeDetect
  public String getCategoryName() {
    return categoryName;
  }

  @ChangeDetect
  public String getCategoryCode() {
    return categoryCode;
  }

  @ChangeDetect
  public Boolean getHasLiveNow() {
    return hasLiveNow;
  }

  @ChangeDetect
  public Boolean getHasUpcoming() {
    return hasUpcoming;
  }

  @ChangeDetect
  public Boolean getHasLiveStream() {
    return hasLiveStream;
  }

  @ChangeDetect
  public String getAlt() {
    return alt;
  }

  @ChangeDetect
  public String getDefaultTab() {
    return defaultTab;
  }

  @ChangeDetect
  public Boolean getDisabled() {
    return disabled;
  }

  @ChangeDetect
  public List<String> getDispSortName() {
    return dispSortName;
  }

  @ChangeDetect
  public String getFileName() {
    return fileName;
  }

  @ChangeDetect
  public Integer getHeightMedium() {
    return heightMedium;
  }

  @ChangeDetect
  public Integer getHeightSmall() {
    return heightSmall;
  }

  @ChangeDetect
  public String getImageTitle() {
    return imageTitle;
  }

  @ChangeDetect
  public Boolean getInApp() {
    return inApp;
  }

  @ChangeDetect
  public Boolean getMultiTemplateSport() {
    return isMultiTemplateSport;
  }

  @ChangeDetect
  public Boolean getOutrightSport() {
    return isOutrightSport;
  }

  @ChangeDetect
  public Map<String, String> getOddsCardHeaderType() {
    return oddsCardHeaderType;
  }

  @ChangeDetect
  public String getPrimaryMarkets() {
    return primaryMarkets;
  }

  @ChangeDetect
  public boolean isShowInPlay() {
    return showInPlay;
  }

  @ChangeDetect
  public String getSsCategoryCode() {
    return ssCategoryCode;
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  public Tab getTabs() {
    return tabs;
  }

  @ChangeDetect
  public List<String> getTypeIds() {
    return typeIds;
  }

  @ChangeDetect
  public String getUriMedium() {
    return uriMedium;
  }

  @ChangeDetect
  public String getUriMediumIcon() {
    return uriMediumIcon;
  }

  @ChangeDetect
  public String getUriSmall() {
    return uriSmall;
  }

  @ChangeDetect
  public String getUriSmallIcon() {
    return uriSmallIcon;
  }

  @ChangeDetect
  public List<String> getViewByFilters() {
    return viewByFilters;
  }

  @ChangeDetect
  public Integer getWidthMedium() {
    return widthMedium;
  }

  @ChangeDetect
  public Integer getWidthSmall() {
    return widthSmall;
  }

  @ChangeDetect
  public String getTargetUri() {
    return targetUri;
  }

  @ChangeDetect
  public String getTargetUriCopy() {
    return targetUriCopy;
  }

  @ChangeDetect
  public int getLiveEventCount() {
    return liveEventCount;
  }

  @ChangeDetect
  public int getLiveStreamEventCount() {
    return liveStreamEventCount;
  }

  @ChangeDetect
  public int getUpcomingEventCount() {
    return upcomingEventCount;
  }

  @ChangeDetect
  public Boolean getHasUpcommingLiveStream() {
    return hasUpcommingLiveStream;
  }

  @ChangeDetect
  public int getUpcommingLiveStreamEventCount() {
    return upcommingLiveStreamEventCount;
  }
}
