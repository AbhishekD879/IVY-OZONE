package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class RacingModule extends AbstractFeaturedModule<RacingModuleConfig> {
  private ModuleType moduleType = ModuleType.RACING_MODULE;

  public RacingModule(SportModule cmsModule) {
    super(cmsModule);
  }

  @Override
  public ModuleType getModuleType() {
    return moduleType;
  }
}
