package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.RacingEventData;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class RacingEventsModule extends AbstractRacingEventsModule<RacingEventData> {

  private String racingType;
  private ModuleType moduleType = ModuleType.RACING_EVENT_MODULE;

  public RacingEventsModule(SportModule cmsModule, String racingType, boolean active) {
    super(cmsModule, active);
    this.racingType = racingType;
  }

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }
}
