package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.EqualsAndHashCode;
import lombok.Setter;
import lombok.ToString;

@Setter
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class SurfaceBetModule extends AbstractFeaturedModule<SurfaceBetModuleData> {

  protected Integer maxRows; // 5,
  protected Integer maxSelections; // 5,
  protected Boolean cashoutAvail; // false
  protected boolean hasNoLiveEvents;
  private List<String> outcomeColumnsTitles;
  protected boolean isYourCallAvailable;
  protected Integer totalEvents; // 36,
  private Map<String, SegmentView> moduleSegmentView = new HashMap<>();
  private Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = new HashMap<>();

  public SurfaceBetModule() {
    this.showExpanded = true;
  }

  @ChangeDetect
  public Integer getMaxRows() {
    return maxRows;
  }

  @ChangeDetect
  public Integer getMaxSelections() {
    return maxSelections;
  }

  @ChangeDetect
  public Boolean getCashoutAvail() {
    return cashoutAvail;
  }

  @ChangeDetect
  public boolean hasNoLiveEvents() {
    return hasNoLiveEvents;
  }

  @ChangeDetect
  public List<String> getOutcomeColumnsTitles() {
    return outcomeColumnsTitles;
  }

  @ChangeDetect
  public boolean isYourCallAvailable() {
    return isYourCallAvailable;
  }

  @ChangeDetect
  public Integer getTotalEvents() {
    return totalEvents;
  }

  @JsonIgnore
  @Override
  public ModuleType getModuleType() {
    return ModuleType.SURFACE_BET;
  }

  public Map<String, SegmentView> getModuleSegmentView() {
    return moduleSegmentView;
  }

  public Map<String, FanzoneSegmentView> getFanzoneModuleSegmentView() {
    return fanzoneModuleSegmentView;
  }

  public SurfaceBetModule copyWithEmptySegmentedData(double segmentOrder) {
    SurfaceBetModule result = (SurfaceBetModule) copyWithEmptyData();
    result.setFanzoneModuleSegmentView(null);
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setSegmentOrder(segmentOrder);
    return result;
  }
}
