package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class TypeSegment {

  private String className;
  private String categoryName;
  private String categoryCode;
  private String typeName;
  private String typeId;
  private Integer classDisplayOrder;
  private Integer typeDisplayOrder;
  private String typeSectionTitleAllSports;
  private String typeSectionTitleOneSport;
  private String typeSectionTitleConnectApp;
  private int eventCount;
  private Collection<Long> eventsIds = new ArrayList<>();
  private List<ModuleDataItem> events;
  private AssetManagementDto assetManagement;

  @JsonIgnore
  public TypeSegment cloneWithEmptyTypes() {
    return new TypeSegment(
        className,
        categoryName,
        categoryCode,
        typeName,
        typeId,
        classDisplayOrder,
        typeDisplayOrder,
        typeSectionTitleAllSports,
        typeSectionTitleOneSport,
        typeSectionTitleConnectApp,
        eventCount,
        eventsIds,
        null,
        assetManagement);
  }

  @JsonIgnore
  public TypeSegment cloneWithEmptyHRTypes() {
    List<ModuleDataItem> eventsData =
        events.stream()
            .map(ModuleDataItem::cloneWithEmptyHREventTypes)
            .collect(Collectors.toList());
    return new TypeSegment(
        className,
        categoryName,
        categoryCode,
        typeName,
        typeId,
        classDisplayOrder,
        typeDisplayOrder,
        typeSectionTitleAllSports,
        typeSectionTitleOneSport,
        typeSectionTitleConnectApp,
        eventCount,
        eventsIds,
        eventsData,
        assetManagement);
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("EventByType{");
    sb.append("className='").append(className).append('\'');
    sb.append(", categoryName='").append(categoryName).append('\'');
    sb.append(", categoryCode='").append(categoryCode).append('\'');
    sb.append(", typeName='").append(typeName).append('\'');
    sb.append(", typeId='").append(typeId).append('\'');
    sb.append(", classDisplayOrder=").append(classDisplayOrder);
    sb.append(", typeDisplayOrder=").append(typeDisplayOrder);
    sb.append(", typeSectionTitleAllSports=").append(typeSectionTitleAllSports);
    sb.append(", typeSectionTitleOneSport=").append(typeSectionTitleOneSport);
    sb.append(", typeSectionTitleConnectApp=").append(typeSectionTitleConnectApp);
    sb.append(", eventsIds=").append(eventsIds);
    sb.append(", eventCount=").append(eventCount);
    sb.append(", events=").append(events);
    sb.append(", assetManagement=").append(assetManagement);
    sb.append('}');
    return sb.toString();
  }
}
