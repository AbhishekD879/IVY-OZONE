package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.InternationalToteRaceData;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class InternationalToteRaceModule
    extends AbstractRacingEventsModule<InternationalToteRaceData> {

  private ModuleType moduleType = ModuleType.RACING_TOTE_MODULE;

  public InternationalToteRaceModule(SportModule cmsModule, boolean active) {
    super(cmsModule, active);
  }

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }
}
