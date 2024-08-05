package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

/**
 * Represents the Module model. Copied from Middleware Service.
 *
 * @author tvuyiv
 */
@Data
@Slf4j
public class OutputModule {

  @JsonProperty("_id")
  private String id;

  private String title;
  private BigDecimal displayOrder;
  private Boolean showExpanded;
  private Integer maxRows;
  private Integer maxSelections;
  private Integer totalEvents;
  private List<String> publishedDevices;
  private List<ModuleDataItem> data;
  private ModuleDataSelection dataSelection;
  private Map<String, String> footerLink;
  private Boolean cashoutAvail;
  private boolean hasNoLiveEvents;
  private List<String> outcomeColumnsTitles;
  private boolean isSpecial;
  private boolean isEnhanced;
  private boolean isYourCallAvailable;
  private String errorMessage;

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    OutputModule that = (OutputModule) o;

    return id.equals(that.id);
  }

  @Override
  public int hashCode() {
    int result = super.hashCode();
    result = 31 * result + id.hashCode();
    return result;
  }
}
