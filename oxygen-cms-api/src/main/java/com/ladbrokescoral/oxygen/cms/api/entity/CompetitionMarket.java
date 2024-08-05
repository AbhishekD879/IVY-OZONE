package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionMarket {

  @NotBlank String marketId;
  @NotBlank String defaultName;
  String nameOverride;
  ViewType viewType;
  boolean collapsed;
  int maxDisplay = 6;
  boolean enabled;
}
