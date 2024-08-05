package com.coral.oxygen.middleware.ms.quickbet.connector.dto;

import io.vavr.collection.List;
import lombok.Value;

@Value
public class ComplexSelection {
  private Type type;
  private List<String> outcomeIds;

  public enum Type {
    SCORECAST("SC"),
    STRAIGHT_FORECAST("SF"),
    REVERSE_FORECAST("RF"),
    COMBINATION_FORECAST("CF"),
    STRAIGHT_TRICAST("TC"),
    COMBINATION_TRICAST("CT");

    private final String legSortCode;

    Type(String legSortCode) {
      this.legSortCode = legSortCode;
    }

    public String getLegSortCode() {
      return legSortCode;
    }
  }
}
