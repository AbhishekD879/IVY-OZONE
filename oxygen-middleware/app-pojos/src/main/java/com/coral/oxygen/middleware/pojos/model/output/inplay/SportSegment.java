package com.coral.oxygen.middleware.pojos.model.output.inplay;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@ToString(callSuper = false)
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "categoryCode")
public class SportSegment extends AbstractModuleData implements Serializable {

  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "SportSegment";

  private Integer categoryId;
  private InPlayTopLevelType topLevelType;
  private boolean showInPlay;
  private String categoryName;
  private String categoryCode;
  private String categoryPath;

  private List<TypeSegment> eventsByTypeName = new ArrayList<>();
  private Collection<Long> eventsIds = new ArrayList<>();

  private Integer displayOrder;
  private String sportUri;
  private String svgId;
  private int eventCount;

  private List<String> marketSelectorOptions;

  private String marketSelector;

  private List<SegmentReference> segmentReferences;
  private boolean used = false;

  @ChangeDetect
  public String getCategoryName() {
    return categoryName;
  }

  public void setCategoryName(String categoryName) {
    this.categoryName = categoryName;
  }

  @ChangeDetect
  public String getCategoryCode() {
    return categoryCode;
  }

  public void setCategoryCode(String categoryCode) {
    this.categoryCode = categoryCode;
  }

  @ChangeDetect
  public String getCategoryPath() {
    return categoryPath;
  }

  public void setCategoryPath(String categoryPath) {
    this.categoryPath = categoryPath;
  }

  @ChangeDetect(compareList = true)
  public List<TypeSegment> getEventsByTypeName() {
    return eventsByTypeName;
  }

  public void setEventsByTypeName(List<TypeSegment> eventsByTypeName) {
    this.eventsByTypeName = eventsByTypeName;
  }

  public Collection<Long> getEventsIds() {
    return eventsIds;
  }

  public void setEventsIds(Collection<Long> eventsIds) {
    this.eventsIds = eventsIds;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public void setDisplayOrder(Integer displayOrder) {
    this.displayOrder = displayOrder;
  }

  @ChangeDetect
  public String getSportUri() {
    return sportUri;
  }

  public void setSvgId(String svgId) {
    this.svgId = svgId;
  }

  @ChangeDetect
  public String getSvgId() {
    return this.svgId;
  }

  public void setSportUri(String sportUri) {
    this.sportUri = sportUri;
  }

  public void setCategoryId(Integer categoryId) {
    this.categoryId = categoryId;
  }

  @ChangeDetect
  public Integer getCategoryId() {
    return categoryId;
  }

  public void setTopLevelType(InPlayTopLevelType topLevelType) {
    this.topLevelType = topLevelType;
  }

  public InPlayTopLevelType getTopLevelType() {
    return topLevelType;
  }

  public void setEventCount(int eventCount) {
    this.eventCount = eventCount;
  }

  public int getEventCount() {
    return eventCount;
  }

  @Override
  public String idForChangeDetection() {
    return Optional.ofNullable(categoryId).map(Objects::toString).orElse(null);
  }

  public static String getKey(SportSegment sportSegment) {
    String result = sportSegment.getCategoryId() + "::" + sportSegment.getTopLevelType();
    if (sportSegment.getMarketSelector() != null) {
      result += "::" + sportSegment.getMarketSelector();
    }
    return result;
  }

  public static List<String> getAllMarketSelectorKeys(SportSegment sportSegment) {
    List<String> result = new ArrayList<>();
    String defaultSelector = sportSegment.getCategoryId() + "::" + sportSegment.getTopLevelType();
    result.add(defaultSelector);
    if (sportSegment.getMarketSelectorOptions() != null) {
      result.addAll(
          sportSegment.getMarketSelectorOptions().stream()
              .map(selector -> defaultSelector + "::" + selector)
              .toList());
    }
    return result;
  }

  public void setShowInPlay(boolean showInPlay) {
    this.showInPlay = showInPlay;
  }

  @ChangeDetect
  public boolean isShowInPlay() {
    return showInPlay;
  }

  public List<String> getMarketSelectorOptions() {
    return marketSelectorOptions;
  }

  @ChangeDetect
  public void setMarketSelectorOptions(List<String> marketSelectorOptions) {
    this.marketSelectorOptions = marketSelectorOptions;
  }

  public String getMarketSelector() {
    return marketSelector;
  }

  public void setMarketSelector(String marketSelector) {
    this.marketSelector = marketSelector;
  }

  public List<SegmentReference> getSegmentReferences() {
    return segmentReferences;
  }

  public void setSegmentReferences(List<SegmentReference> segmentReferences) {
    this.segmentReferences = segmentReferences;
  }

  public boolean isUsed() {
    return used;
  }

  public void setUsed(boolean used) {
    this.used = used;
  }
}
