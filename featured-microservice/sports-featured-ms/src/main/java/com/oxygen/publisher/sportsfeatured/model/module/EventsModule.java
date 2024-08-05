package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.ModuleType;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.ModuleDataSelection;
import com.oxygen.publisher.sportsfeatured.visitor.FeaturedModuleVisitor;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Data
@Slf4j
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class EventsModule extends AbstractFeaturedModule<EventsModuleData> {

  private String type = "EventsModule";
  private Integer maxRows;
  private Integer maxSelections;
  private Integer totalEvents;
  private ModuleDataSelection dataSelection;
  private Map<String, String> footerLink;
  private Boolean cashoutAvail;
  private boolean hasNoLiveEvents;
  private List<String> outcomeColumnsTitles;
  private String categoryId;

  private boolean isSpecial;
  private boolean isEnhanced;
  private boolean isYourCallAvailable;
  private boolean groupedBySport;

  @Override
  public ModuleType getModuleType() {
    return ModuleType.FEATURED;
  }

  @Override
  public void accept(FeaturedModuleVisitor visitor) {
    visitor.visit(this);
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

  public EventsModule copyWithData(double segmentOrder) {
    EventsModule result = copyWithEmptySegmentedData(segmentOrder);
    result.setData(
        this.getData().stream()
            .map(EventsModuleData::cloneWithNewUniqueId)
            .collect(Collectors.toList()));
    return result;
  }
}
