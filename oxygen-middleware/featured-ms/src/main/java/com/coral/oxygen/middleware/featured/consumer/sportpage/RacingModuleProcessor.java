package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.featured.consumer.sportpage.racing.InternationalToteRacingModuleService;
import com.coral.oxygen.middleware.featured.consumer.sportpage.racing.RacingEventModuleService;
import com.coral.oxygen.middleware.featured.consumer.sportpage.racing.VirtualCarouselRacingModuleService;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.RacingModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.RacingModuleConfig;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class RacingModuleProcessor implements ModuleConsumer<AbstractFeaturedModule<?>> {

  private final RacingEventModuleService racingEventService;
  private final VirtualCarouselRacingModuleService virtualCarouselService;
  private final InternationalToteRacingModuleService internationalToteService;

  /**
   * Cms racing module page data contains 1 racing config, though 1 featured module will be
   * returned. In case, cms configurations is changed and we receive more than 1 racing config of
   * different types, then multiple featured modules will be produced.
   *
   * @param cmsModule - contins sport module and list of page-data (here racing configs)
   * @param systemConfig - ignored
   * @param excludedEventIds - ignored
   * @return list of featured modules, separate module for different racing module type
   */
  @Override
  public List<AbstractFeaturedModule<?>> processModules(
      SportPageModule cmsModule, CmsSystemConfig systemConfig, Set<Long> excludedEventIds) {
    try {
      Map<String, List<CmsRacingModule>> byRacingConfigType =
          cmsModule.getPageData().stream()
              .map(CmsRacingModule.class::cast)
              .filter(
                  m ->
                      Objects.nonNull(m.getRacingConfig())
                          && Objects.nonNull(m.getRacingConfig().getAbbreviation()))
              .collect(Collectors.groupingBy(data -> data.getRacingConfig().getAbbreviation()));
      return byRacingConfigType.entrySet().stream()
          .map(e -> toFeaturedRacingModule(cmsModule, e.getKey(), e.getValue()))
          .collect(Collectors.toList());
    } catch (Exception e) {
      log.error("Failed to create Racing Module {}", cmsModule.getSportModule().getTitle(), e);
      return Collections.emptyList();
    }
  }

  private AbstractFeaturedModule<?> toFeaturedRacingModule(
      SportPageModule cmsModule, String racingModuleType, List<CmsRacingModule> racingConfigs) {
    RacingModuleType racingType = RacingModuleType.from(racingModuleType);
    switch (racingType) {
      case VIRTUAL_RACE_CAROUSEL:
        return virtualCarouselService.getFeaturedModule(cmsModule.getSportModule(), racingConfigs);
      case INTERNATIONAL_TOTE_CAROUSEL:
        return internationalToteService.getFeaturedModule(
            cmsModule.getSportModule(), racingConfigs);
      case UK_AND_IRISH_RACES:
      case INTERNATIONAL_RACES:
      case LEGENDS_VIRTUAL_RACES:
        return racingEventService.getFeaturedModule(
            cmsModule.getSportModule(), racingConfigs, racingType);
      default:
        return getRacingModule(cmsModule.getSportModule(), racingConfigs);
    }
  }

  private RacingModule getRacingModule(SportModule cmsModule, List<CmsRacingModule> racingConfigs) {
    RacingModule racingModule = new RacingModule(cmsModule);
    racingModule.setData(
        racingConfigs.stream().map(RacingModuleConfig::new).collect(Collectors.toList()));
    return racingModule;
  }
}
