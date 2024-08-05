package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@Slf4j
@RequiredArgsConstructor
public class SportTabEventCheckerConfig {

  private static final String LADBROKES_BRAND = "ladbrokes";
  private static final String CORAL_BRAND = "bma";

  private final SiteServeService siteServeService;
  private final SportTabService sportTabService;
  private final ScheduledTaskExecutor scheduledTaskExecutor;
  private final TierCategoriesCache tierCategoriesCache;

  @Bean
  EventsChecker ladbrokesCompetitionsTabChecker() {
    return new CompetitionsEventsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }

  @Bean
  EventsChecker coralCompetitionsTabChecker() {
    return new CompetitionsEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker ladbrokesCouponsTabChecker() {
    return new CouponsTabEventsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }

  @Bean
  EventsChecker coralCouponsTabChecker() {
    return new CouponsTabEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker ladbrokesSpecialsChecker() {
    return new SpecialsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }

  @Bean
  EventsChecker coralSpecialsChecker() {
    return new SpecialsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker footballJackpotTabEventsChecker() {
    return new JackpotTabEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache);
  }

  @Bean
  EventsChecker ladbrokesMatchesTabEventsChecker() {
    return new MatchesTabEventsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }

  @Bean
  EventsChecker coralMatchesTabEventsChecker() {
    return new MatchesTabEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker ladbrokesOutrightsTabEventsChecker() {
    return new OutrightsTabEventsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }

  @Bean
  EventsChecker coralOutrightsTabEventsChecker() {
    return new OutrightsTabEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker ladsGolfMatchesTabEventsChecker() {
    return new GolfMatchesTabEventsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }

  @Bean
  EventsChecker coralGolfMatchesTabEventsChecker() {
    return new GolfMatchesTabEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker coralGolfInPlayTabEventsChecker() {
    return new GolfInplayTabEventsChecker(
        scheduledTaskExecutor, siteServeService, sportTabService, tierCategoriesCache, CORAL_BRAND);
  }

  @Bean
  EventsChecker ladsGolfInPlayTabEventsChecker() {
    return new GolfInplayTabEventsChecker(
        scheduledTaskExecutor,
        siteServeService,
        sportTabService,
        tierCategoriesCache,
        LADBROKES_BRAND);
  }
}
