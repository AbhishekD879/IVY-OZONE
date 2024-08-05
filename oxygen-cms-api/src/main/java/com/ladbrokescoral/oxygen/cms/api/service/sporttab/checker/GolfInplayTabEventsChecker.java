package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public class GolfInplayTabEventsChecker extends EventsChecker {
  private final SiteServeService siteServeService;
  private final String brand;

  public GolfInplayTabEventsChecker(
      ScheduledTaskExecutor scheduledTaskExecutor,
      SiteServeService siteServeService,
      SportTabService sportTabService,
      TierCategoriesCache tierCategoriesCache,
      String brand) {
    super(scheduledTaskExecutor, sportTabService, tierCategoriesCache);
    this.siteServeService = siteServeService;
    this.brand = brand;
  }

  @Override
  protected void doCheck() {
    List<SportTab> golfInPlayMatchesTabs =
        sportTabService.findAllForCheckingEvents(brand, SportTabNames.LIVE);
    Map<Integer, SportCategory> tier2Sports =
        tierCategoriesCache.getCategories(brand, SportTier.TIER_2).stream()
            .collect(Collectors.toMap(SportCategory::getCategoryId, Function.identity()));

    golfInPlayMatchesTabs.forEach(
        tab ->
            tier2Sports.computeIfPresent(
                tab.getSportId(),
                (Integer sportId, SportCategory sport) -> {
                  boolean hasEvents =
                      ((SiteServeServiceImpl) siteServeService)
                          .anyLiveOrUpcomingTodaysEventsExistsForGolf(sport);
                  adjustHasEventsValue(tab, hasEvents);
                  return sport;
                }));
  }
}
