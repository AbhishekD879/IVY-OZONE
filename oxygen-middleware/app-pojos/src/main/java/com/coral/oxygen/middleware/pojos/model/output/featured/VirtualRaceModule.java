package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.VirtualRaceModuleData;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class VirtualRaceModule extends AbstractRacingEventsModule<VirtualRaceModuleData> {

  private ModuleType moduleType = ModuleType.RACING_MODULE;

  public VirtualRaceModule(SportModule cmsModule, boolean isActive) {
    super(cmsModule, isActive);
  }

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }
}
