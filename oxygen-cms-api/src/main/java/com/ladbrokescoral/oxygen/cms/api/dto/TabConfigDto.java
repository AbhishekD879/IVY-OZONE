package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.util.Map;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;

@Getter
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@EqualsAndHashCode
@JsonInclude(JsonInclude.Include.NON_NULL)
public class TabConfigDto {

  @JsonProperty("tabs")
  private Map<String, SSTabRequestFilters> tabRequestsFilters;

  // FIXME: need rework. use lombok
  public static Builder builder() {
    return new Builder();
  }

  // FIXME: need rework. use lombok
  public static class Builder {

    private TabFiltersBuilder tabFiltersBuilder;

    public Builder config(SportCategory sportCategory) {
      tabFiltersBuilder = new TabFiltersBuilder(sportCategory);
      tabFiltersBuilder.build();
      return this;
    }

    public TabConfigDto build() {
      return new TabConfigDto(tabFiltersBuilder.getTabRequestsFilters());
    }
  }
}
