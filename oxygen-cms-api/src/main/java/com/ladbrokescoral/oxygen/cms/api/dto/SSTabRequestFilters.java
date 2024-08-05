package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
class SSTabRequestFilters {

  private String date;

  @JsonProperty("isActive")
  private Boolean active;

  private Boolean marketsCount;

  @JsonProperty("isNotStarted")
  private Boolean notStarted;

  @JsonProperty("marketDrilldownTagNamesContains")
  private String drilldownTagNames;

  private Boolean templateMarketNameOnlyIntersects;
}
