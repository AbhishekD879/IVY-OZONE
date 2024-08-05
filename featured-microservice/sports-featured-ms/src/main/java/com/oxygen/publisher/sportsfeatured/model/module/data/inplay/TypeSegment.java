package com.oxygen.publisher.sportsfeatured.model.module.data.inplay;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.model.AssetManagementDto;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "typeId")
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
  private List<EventsModuleData> events;
  private AssetManagementDto assetManagement;

  public com.oxygen.publisher.model.TypeSegment cloneWithEmptyTypes() {
    return new com.oxygen.publisher.model.TypeSegment(
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

  public TypeSegment cloneWithEmptyEvents() {
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
        null,
        null,
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
