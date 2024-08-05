package com.coral.oxygen.middleware.pojos.model.output.featured;

import static com.coral.oxygen.middleware.pojos.model.cms.EventLoadingType.RACING_GRID;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.Module;
import com.coral.oxygen.middleware.pojos.model.cms.ModuleDataSelection;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class EventsModule extends AbstractSegmentEventModule {

  private static final String BADGE_SPECIALS = "specials";
  private static final String BADGE_ENHANCED = "enhanced";

  protected Integer maxRows; // 5,
  protected Integer maxSelections; // 5,
  private ModuleDataSelection dataSelection; // {"selectionType": "Type","selectionId": "435"},
  private Map<String, String> footerLink; // {"text": "","url": ""},
  protected Boolean cashoutAvail; // false
  protected boolean hasNoLiveEvents;
  private List<String> outcomeColumnsTitles;
  protected boolean isSpecial;
  protected boolean isEnhanced;
  protected boolean isYourCallAvailable;
  protected Integer totalEvents; // 36,
  protected String categoryId;
  protected boolean groupedBySport;
  protected ModuleType moduleType = ModuleType.FEATURED;

  public EventsModule() {
    if (hasStaticContent()) {
      throw new IllegalArgumentException("The container should have dynamic content.");
    }
  }

  public EventsModule(SportModule sportModule, Module section) {
    this.id = section.get_id();
    this.title = section.getTitle();
    this.displayOrder = sportModule.getSortOrderOrDefault(null);
    this.secondaryDisplayOrder = section.getDisplayOrder();
    this.showExpanded = section.getShowExpanded();
    try {
      this.maxSelections = Integer.parseInt(section.getMaxSelections());
    } catch (Exception e) {
      // suppress
    }
    this.totalEvents = section.getTotalEvents();
    setPublishedDevices(section.getPublishedDevices());
    setData(new ArrayList<>(section.getData()));
    this.dataSelection = section.getDataSelection();
    this.footerLink = section.getFooterLink();
    this.maxRows = section.getMaxRows();
    this.groupedBySport = section.isGroupedBySport();
    String badge = section.getBadge();
    if (badge != null) {
      this.isSpecial = badge.toLowerCase().contains(BADGE_SPECIALS);
      this.isEnhanced = badge.toLowerCase().contains(BADGE_ENHANCED);
    }
    this.pageType = sportModule.getPageType();
    this.moduleType = sportModule.getModuleType();
    this.setSegments(section.getSegments());
    this.setSegmentReferences(section.getSegmentReferences());
  }

  @ChangeDetect
  public Integer getTotalEvents() {
    return totalEvents;
  }

  public void setTotalEvents(Integer totalEvents) {
    this.totalEvents = totalEvents;
  }

  @Override
  @ChangeDetect
  public Boolean getShowExpanded() {
    return showExpanded;
  }

  @ChangeDetect
  public Integer getMaxSelections() {
    return maxSelections;
  }

  public void setMaxSelections(Integer maxSelections) {
    this.maxSelections = maxSelections;
  }

  @ChangeDetect(compareNestedObject = true)
  public ModuleDataSelection getDataSelection() {
    return dataSelection;
  }

  public void setDataSelection(ModuleDataSelection dataSelection) {
    this.dataSelection = dataSelection;
  }

  @ChangeDetect
  public Map<String, String> getFooterLink() {
    return footerLink;
  }

  public void setFooterLink(Map<String, String> footerLink) {
    this.footerLink = footerLink;
  }

  @ChangeDetect
  public Boolean getCashoutAvail() {
    return cashoutAvail;
  }

  public void setCashoutAvail(Boolean cashoutAvail) {
    this.cashoutAvail = cashoutAvail;
  }

  @JsonProperty(value = "isSpecial")
  @ChangeDetect
  public Boolean getSpecial() {
    return isSpecial;
  }

  public void setSpecial(boolean isSpecial) {
    this.isSpecial = isSpecial;
  }

  @JsonProperty(value = "isEnhanced")
  @ChangeDetect
  public Boolean getEnhanced() {
    return isEnhanced;
  }

  public void setEnhanced(boolean isEnhanced) {
    this.isEnhanced = isEnhanced;
  }

  @ChangeDetect
  public Integer getMaxRows() {
    return maxRows;
  }

  public boolean hasNoLiveEvents() {
    return hasNoLiveEvents;
  }

  public void setHasNoLiveEvents(boolean hasNoLiveEvents) {
    this.hasNoLiveEvents = hasNoLiveEvents;
  }

  public List<String> getOutcomeColumnsTitles() {
    return outcomeColumnsTitles;
  }

  public void setOutcomeColumnsTitles(List<String> outcomeColumnsTitles) {
    this.outcomeColumnsTitles = outcomeColumnsTitles;
  }

  @JsonProperty(value = "isYourCallAvailable")
  @ChangeDetect
  public boolean isYourCallAvailable() {
    return isYourCallAvailable;
  }

  public void setYourCallAvailable(boolean yourCallAvailable) {
    isYourCallAvailable = yourCallAvailable;
  }

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }

  public String getCategoryId() {
    return categoryId;
  }

  public void setCategoryId(String categoryId) {
    this.categoryId = categoryId;
  }

  public boolean isGroupedBySport() {
    return groupedBySport;
  }

  public void setGroupedBySport(boolean groupedBySport) {
    this.groupedBySport = groupedBySport;
  }

  /*
   * isEventModuleWithRacingGridSelection used for filter modules in createModule method
   * vkulpa: BMA-39330 says EventModule without events (dataSelection RacingGrid only) should be in WS
   * later might be story to remove such modules but not now...
   */
  @Override
  public boolean isValid() {
    return RACING_GRID.getValue().equals(getDataSelection().getSelectionType()) || super.isValid();
  }

  public EventsModule copyWithData(double segmentOrder) {
    EventsModule result = copyWithEmptySegmentedData(segmentOrder);
    result.setData(this.getData().stream().map(EventsModuleData::cloneWithNewUniqueId).toList());
    return result;
  }

  public EventsModule copyWithEmptySegmentedData(double segmentOrder) {
    EventsModule result = (EventsModule) copyWithEmptyData();
    result.setFanzoneModuleSegmentView(null);
    result.setModuleSegmentView(null);
    result.setSegments(null);
    result.setSegmentOrder(segmentOrder);
    result.setFanzoneSegments(null);
    return result;
  }
}
