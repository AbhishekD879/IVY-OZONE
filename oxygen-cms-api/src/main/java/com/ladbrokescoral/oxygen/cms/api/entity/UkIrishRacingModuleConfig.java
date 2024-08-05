package com.ladbrokescoral.oxygen.cms.api.entity;

import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.UK_AND_IRISH_RACES;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class UkIrishRacingModuleConfig extends RacingEventsModuleConfig {

  private boolean enablePoolIndicators = true;

  public UkIrishRacingModuleConfig() {
    super();
    setType(UK_AND_IRISH_RACES);
  }
}
