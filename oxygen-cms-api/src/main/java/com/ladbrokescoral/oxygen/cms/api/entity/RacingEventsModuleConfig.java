package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class RacingEventsModuleConfig extends RacingModuleConfig {

  private int eventsSelectionDays;
}
