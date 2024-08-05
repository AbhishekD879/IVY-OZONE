package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SportSegment {

  private Integer categoryId;
  private String topLevelType;
  private boolean showInPlay;
  private String categoryName;
  private String categoryCode;
  private String categoryPath;
  private List<TypeSegment> eventsByTypeName;
  private Collection<Integer> eventsIds;
  private Integer displayOrder;
  private String sportUri;
  private String svgId;
  private int eventCount;
  private List<String> marketSelectorOptions;
  private String marketSelector;

  @JsonIgnore
  public SportSegment getCloneWithEmptyTypes() {
    List<TypeSegment> cloneEventsByTypeName =
        eventsByTypeName.stream()
            .map(TypeSegment::cloneWithEmptyTypes)
            .collect(Collectors.toList());
    return new SportSegment(
        categoryId,
        topLevelType,
        showInPlay,
        categoryName,
        categoryCode,
        categoryPath,
        cloneEventsByTypeName,
        eventsIds,
        displayOrder,
        sportUri,
        svgId,
        eventCount,
        marketSelectorOptions,
        marketSelector);
  }

  @JsonIgnore
  public SportSegment getCloneWithEmptyHRTypes() {
    List<TypeSegment> cloneEventsByTypeName =
        eventsByTypeName.stream()
            .map(TypeSegment::cloneWithEmptyHRTypes)
            .collect(Collectors.toList());
    return new SportSegment(
        categoryId,
        topLevelType,
        showInPlay,
        categoryName,
        categoryCode,
        categoryPath,
        cloneEventsByTypeName,
        eventsIds,
        displayOrder,
        sportUri,
        svgId,
        eventCount,
        marketSelectorOptions,
        marketSelector);
  }
}
