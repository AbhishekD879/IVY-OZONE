package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum SelectionType {
  CATEGORY("Category", true),
  CLASS("Class", true),
  TYPE("Type", true),
  RACE_TYPE_ID("RaceTypeId", true),
  SELECTION("Selection"),
  ENHANCED_MULTIPLES("Enhanced Multiples", true),
  MARKET("Market"),
  EVENT("Event"),
  ALL("All");

  private String value;
  private boolean autoRefreshSupported;

  SelectionType(String value) {
    this.value = value;
  }

  public static SelectionType fromString(String value) {
    for (SelectionType type : SelectionType.values()) {
      if (type.getValue().equalsIgnoreCase(value)) {
        return type;
      }
    }
    throw new IllegalArgumentException(
        String.format("SelectionType with %s value does not exist", value));
  }

  public static boolean isAutoRefreshSupported(String value) {
    return Stream.of(SelectionType.values())
        .filter(t -> t.getValue().equalsIgnoreCase(value))
        .findAny()
        .map(SelectionType::isAutoRefreshSupported)
        .orElse(false);
  }

  public static List<String> getAutoRefreshTypes() {
    return Arrays.stream(values())
        .filter(SelectionType::isAutoRefreshSupported)
        .map(SelectionType::getValue)
        .collect(Collectors.toList());
  }
}
