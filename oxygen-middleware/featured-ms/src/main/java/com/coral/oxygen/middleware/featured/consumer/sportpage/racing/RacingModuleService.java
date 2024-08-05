package com.coral.oxygen.middleware.featured.consumer.sportpage.racing;

import com.coral.oxygen.middleware.featured.consumer.sportpage.RacingModuleType;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import java.util.List;

public interface RacingModuleService<
    E extends AbstractModuleData, T extends AbstractFeaturedModule<E>> {
  T getFeaturedModule(SportModule cmsModule, List<CmsRacingModule> racingConfigs);

  T getFeaturedModule(
      SportModule cmsModule,
      List<CmsRacingModule> racingConfigs,
      RacingModuleType racingModuleType);
}
