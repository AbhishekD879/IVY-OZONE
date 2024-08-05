package com.coral.oxygen.middleware.pojos.model.output.inplay;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

@NoArgsConstructor
@AllArgsConstructor
@Slf4j
@Data
@Getter(AccessLevel.NONE)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "typeId")
public class TypeSegment implements Serializable, Cloneable {

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
  private List<EventsModuleData> events = new ArrayList<>();

  @Setter @Getter private AssetManagement assetManagement;

  @ChangeDetect
  public String getClassName() {
    return className;
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
  public String getTypeName() {
    return typeName;
  }

  public Integer getClassDisplayOrder() {
    return classDisplayOrder;
  }

  public Integer getTypeDisplayOrder() {
    return typeDisplayOrder;
  }

  @ChangeDetect(compareCollection = true)
  public List<EventsModuleData> getEvents() {
    return events;
  }

  public Collection<Long> getEventsIds() {
    return eventsIds;
  }

  public int getEventCount() {
    return eventCount;
  }

  public String getTypeSectionTitleAllSports() {
    return typeSectionTitleAllSports;
  }

  public String getTypeSectionTitleOneSport() {
    return typeSectionTitleOneSport;
  }

  public String getTypeSectionTitleConnectApp() {
    return typeSectionTitleConnectApp;
  }

  public String getTypeId() {
    return this.typeId;
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
}
