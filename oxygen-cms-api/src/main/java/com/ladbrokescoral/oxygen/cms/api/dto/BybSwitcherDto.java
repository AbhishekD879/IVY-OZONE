package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class BybSwitcherDto {
  private String name;
  private Boolean enabled;

  @JsonProperty("default")
  private Boolean defaultValue;

  private String provider;
}
