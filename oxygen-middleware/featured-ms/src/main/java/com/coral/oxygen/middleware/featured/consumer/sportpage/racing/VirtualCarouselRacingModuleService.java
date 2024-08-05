package com.coral.oxygen.middleware.featured.consumer.sportpage.racing;

import com.coral.oxygen.middleware.common.mappers.RacingModuleDataMapper;
import com.coral.oxygen.middleware.featured.consumer.sportpage.RacingModuleType;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RacingConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.VirtualRaceModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.VirtualRaceModule;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class VirtualCarouselRacingModuleService
    extends AbstractRacingModuleService<VirtualRaceModuleData, VirtualRaceModule> {

  private final FeaturedSiteServerService siteServerService;
  private final RacingModuleDataMapper racingEventMapper;

  @Override
  protected VirtualRaceModule createModule(
      SportModule cmsModule, RacingModuleType racingModuleType, boolean active) {
    return new VirtualRaceModule(cmsModule, active);
  }

  @Override
  protected List<VirtualRaceModuleData> getData(
      SportModule cmsModule,
      List<CmsRacingModule> racingConfigs,
      RacingModuleType racingModuleType) {
    return getVirtualEvents(racingConfigs);
  }

  private List<VirtualRaceModuleData> getVirtualEvents(List<CmsRacingModule> racingConfigs) {
    RacingConfig currentConfig = racingConfigs.get(0).getRacingConfig();

    return siteServerService
        .getNextRaces(
            String.valueOf(currentConfig.getClassId()),
            StringUtils.deleteWhitespace(currentConfig.getExcludeTypeIds()))
        .stream()
        .limit(currentConfig.getLimit())
        .map(racingEventMapper::mapVirtualCarouselData)
        .collect(Collectors.toList());
  }
}
