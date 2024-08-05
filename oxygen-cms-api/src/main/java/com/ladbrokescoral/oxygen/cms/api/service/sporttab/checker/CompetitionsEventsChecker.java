package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class CompetitionsEventsChecker extends EventsChecker {
  private final SiteServeService ssService;
  private final String brand;

  public CompetitionsEventsChecker(
      ScheduledTaskExecutor scheduledTaskExecutor,
      SiteServeService ssService,
      SportTabService sportTabService,
      TierCategoriesCache tierCategoriesCache,
      String brand) {
    super(scheduledTaskExecutor, sportTabService, tierCategoriesCache);
    this.ssService = ssService;
    this.brand = brand;
  }

  @Override
  protected void doCheck() {
    List<SportTab> competitionTabs =
        sportTabService.findAllForCheckingEvents(brand, SportTabNames.COMPETITIONS);
    Set<Integer> tabSportIds = extractSportIds(competitionTabs);

    List<SportCategory> sportsWithCompetitionTabs =
        tierCategoriesCache.getCategories(brand, SportTier.TIER_2).stream()
            .filter(sport -> tabSportIds.contains(sport.getCategoryId()))
            .collect(Collectors.toList());

    Set<Integer> categoriesWithCompetitions =
        ssService.filterByCompetitionEvents(brand, sportsWithCompetitionTabs);
    log.trace(
        "Brand: {}. Categories with Competitions events: {}", brand, categoriesWithCompetitions);

    competitionTabs.forEach(
        tab -> {
          boolean hasEvents = categoriesWithCompetitions.contains(tab.getSportId());
          adjustHasEventsValue(tab, hasEvents);
        });
  }
}
