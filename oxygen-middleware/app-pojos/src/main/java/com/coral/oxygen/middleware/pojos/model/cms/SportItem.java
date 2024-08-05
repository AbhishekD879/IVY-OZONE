package com.coral.oxygen.middleware.pojos.model.cms;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class SportItem {

  private String alt;
  private String categoryId;
  private String defaultTab;
  private Boolean disabled;

  private List<String> dispSortName;

  @SerializedName("filename")
  @JsonProperty("filename")
  private String fileName;

  private Integer heightMedium;
  private Integer heightSmall;
  private String imageTitle;
  private String categoryPath;
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

  private List<String> typeIds;
  private String uriMedium;
  private String uriMediumIcon;
  private String uriSmall;
  private String uriSmallIcon;
  private List<String> viewByFilters;
  private Integer widthMedium;
  private Integer widthSmall;

  public String getAlt() {
    return alt;
  }

  public void setAlt(String alt) {
    this.alt = alt;
  }

  public String getCategoryId() {
    return categoryId;
  }

  public void setCategoryId(String categoryId) {
    this.categoryId = categoryId;
  }

  public String getDefaultTab() {
    return defaultTab;
  }

  public void setDefaultTab(String defaultTab) {
    this.defaultTab = defaultTab;
  }

  public boolean isDisabled() {
    return Boolean.TRUE.equals(disabled);
  }

  public void setDisabled(Boolean disabled) {
    this.disabled = disabled;
  }

  public List<String> getDispSortName() {
    return dispSortName;
  }

  public void setDispSortName(List<String> dispSortName) {
    this.dispSortName = dispSortName;
  }

  public String getFileName() {
    return fileName;
  }

  public void setFileName(String fileName) {
    this.fileName = fileName;
  }

  public Integer getHeightMedium() {
    return heightMedium;
  }

  public void setHeightMedium(Integer heightMedium) {
    this.heightMedium = heightMedium;
  }

  public Integer getHeightSmall() {
    return heightSmall;
  }

  public void setHeightSmall(Integer heightSmall) {
    this.heightSmall = heightSmall;
  }

  public String getImageTitle() {
    return imageTitle;
  }

  public void setImageTitle(String imageTitle) {
    this.imageTitle = imageTitle;
  }

  public Boolean getInApp() {
    return inApp;
  }

  public void setInApp(Boolean inApp) {
    this.inApp = inApp;
  }

  public Boolean getMultiTemplateSport() {
    return isMultiTemplateSport;
  }

  public void setMultiTemplateSport(Boolean multiTemplateSport) {
    isMultiTemplateSport = multiTemplateSport;
  }

  public Boolean getOutrightSport() {
    return isOutrightSport;
  }

  public void setOutrightSport(Boolean outrightSport) {
    isOutrightSport = outrightSport;
  }

  public Map<String, String> getOddsCardHeaderType() {
    return oddsCardHeaderType;
  }

  public void setOddsCardHeaderType(Map<String, String> oddsCardHeaderType) {
    this.oddsCardHeaderType = oddsCardHeaderType;
  }

  public String getPrimaryMarkets() {
    return primaryMarkets;
  }

  public void setPrimaryMarkets(String primaryMarkets) {
    this.primaryMarkets = primaryMarkets;
  }

  public boolean isShowInPlay() {
    return showInPlay;
  }

  public void setShowInPlay(boolean showInPlay) {
    this.showInPlay = showInPlay;
  }

  public String getSsCategoryCode() {
    return ssCategoryCode;
  }

  public void setSsCategoryCode(String ssCategoryCode) {
    this.ssCategoryCode = ssCategoryCode;
  }

  public String getSvgId() {
    return svgId;
  }

  public void setSvgId(String svgId) {
    this.svgId = svgId;
  }

  public Tab getTabs() {
    return tabs;
  }

  public void setTabs(Tab tabs) {
    this.tabs = tabs;
  }

  public List<String> getTypeIds() {
    return typeIds;
  }

  public void setTypeIds(List<String> typeIds) {
    this.typeIds = typeIds;
  }

  public String getUriMedium() {
    return uriMedium;
  }

  public void setUriMedium(String uriMedium) {
    this.uriMedium = uriMedium;
  }

  public String getUriMediumIcon() {
    return uriMediumIcon;
  }

  public void setUriMediumIcon(String uriMediumIcon) {
    this.uriMediumIcon = uriMediumIcon;
  }

  public String getUriSmall() {
    return uriSmall;
  }

  public void setUriSmall(String uriSmall) {
    this.uriSmall = uriSmall;
  }

  public String getUriSmallIcon() {
    return uriSmallIcon;
  }

  public void setUriSmallIcon(String uriSmallIcon) {
    this.uriSmallIcon = uriSmallIcon;
  }

  public List<String> getViewByFilters() {
    return viewByFilters;
  }

  public void setViewByFilters(List<String> viewByFilters) {
    this.viewByFilters = viewByFilters;
  }

  public Integer getWidthMedium() {
    return widthMedium;
  }

  public void setWidthMedium(Integer widthMedium) {
    this.widthMedium = widthMedium;
  }

  public Integer getWidthSmall() {
    return widthSmall;
  }

  public void setWidthSmall(Integer widthSmall) {
    this.widthSmall = widthSmall;
  }

  public String getTargetUri() {
    return targetUri;
  }

  public void setTargetUri(String targetUri) {
    this.targetUri = targetUri;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("SportItem{");
    sb.append("alt='").append(alt).append('\'');
    sb.append(", categoryId='").append(categoryId).append('\'');
    sb.append(", defaultTab='").append(defaultTab).append('\'');
    sb.append(", disabled=").append(disabled);
    sb.append(", dispSortName=").append(dispSortName);
    sb.append(", fileName='").append(fileName).append('\'');
    sb.append(", heightMedium=").append(heightMedium);
    sb.append(", heightSmall=").append(heightSmall);
    sb.append(", imageTitle='").append(imageTitle).append('\'');
    sb.append(", inApp=").append(inApp);
    sb.append(", isMultiTemplateSport=").append(isMultiTemplateSport);
    sb.append(", isOutrightSport=").append(isOutrightSport);
    sb.append(", oddsCardHeaderType=").append(oddsCardHeaderType);
    sb.append(", primaryMarkets='").append(primaryMarkets).append('\'');
    sb.append(", showInPlay=").append(showInPlay);
    sb.append(", ssCategoryCode='").append(ssCategoryCode).append('\'');
    sb.append(", svgId='").append(svgId).append('\'');
    sb.append(", tabs=").append(tabs);
    sb.append(", targetUri=").append(targetUri);
    sb.append(", typeIds=").append(typeIds);
    sb.append(", uriMedium='").append(uriMedium).append('\'');
    sb.append(", uriMediumIcon='").append(uriMediumIcon).append('\'');
    sb.append(", uriSmall='").append(uriSmall).append('\'');
    sb.append(", uriSmallIcon='").append(uriSmallIcon).append('\'');
    sb.append(", viewByFilters=").append(viewByFilters);
    sb.append(", widthMedium=").append(widthMedium);
    sb.append(", widthSmall=").append(widthSmall);
    sb.append('}');
    return sb.toString();
  }
}
