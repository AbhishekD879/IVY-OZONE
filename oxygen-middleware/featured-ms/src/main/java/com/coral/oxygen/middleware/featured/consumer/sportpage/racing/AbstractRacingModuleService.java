package com.coral.oxygen.middleware.featured.consumer.sportpage.racing;

import com.coral.oxygen.middleware.featured.consumer.sportpage.RacingModuleType;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public abstract class AbstractRacingModuleService<
        E extends AbstractModuleData, T extends AbstractFeaturedModule<E>>
    implements RacingModuleService<E, T> {

  @Override
  public T getFeaturedModule(SportModule cmsModule, List<CmsRacingModule> racingConfigs) {
    return getFeaturedModule(cmsModule, racingConfigs, null);
  }

  @Override
  public T getFeaturedModule(
      SportModule cmsModule,
      List<CmsRacingModule> racingConfigs,
      RacingModuleType racingModuleType) {
    boolean active = racingConfigs.stream().anyMatch(CmsRacingModule::isActive);
    T racingModule = createModule(cmsModule, racingModuleType, active);
    if (active) {
      racingModule.setData(getData(cmsModule, racingConfigs, racingModuleType));
    }
    return racingModule;
  }

  protected abstract T createModule(
      SportModule cmsModule, RacingModuleType racingModuleType, boolean active);

  protected abstract List<E> getData(
      SportModule cmsModule,
      List<CmsRacingModule> racingConfigs,
      RacingModuleType racingModuleType);
}
