package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import javax.validation.constraints.NotNull;
import lombok.AccessLevel;
import lombok.Data;
import lombok.Getter;

@Data
public class BetPackFilterDto {
  private String id;
  @NotNull private String filterName;
  @NotNull private String brand;
  @NotNull private boolean filterActive;
  private Double sortOrder;

  @Getter(AccessLevel.NONE)
  @NotNull
  private boolean isLinkedFilter;

  @JsonProperty("isLinkedFilter")
  public boolean isLinkedFilter() {
    return isLinkedFilter;
  }

  private String linkedFilterWarningText;
}
