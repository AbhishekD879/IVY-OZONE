package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class SportTabsDto {
  @JsonProperty("tab-live")
  private TabDto tabLive;

  @JsonProperty("tab-matches")
  private TabDto tabMatches;

  @JsonProperty("tab-outrights")
  private TabDto tabOutrights;

  @JsonProperty("tab-specials")
  private TabDto tabSpecials;
}
