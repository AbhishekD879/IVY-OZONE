package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.MainTier2Sports;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class MatchesTabEventsChecker extends EventsChecker {

  private final SiteServeService siteServeService;
  private final String brand;

  public MatchesTabEventsChecker(
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
    List<SportTab> matchesTabs =
        sportTabService.findAllForCheckingEvents(brand, SportTabNames.MATCHES);
    Map<Integer, SportCategory> tier2Sports =
        tierCategoriesCache.getCategories(brand, SportTier.TIER_2).stream()
            .collect(Collectors.toMap(SportCategory::getCategoryId, Function.identity()));
    matchesTabs.forEach(
        tab ->
            tier2Sports.computeIfPresent(
                tab.getSportId(),
                (Integer sportId, SportCategory sport) -> {
                  boolean hasEvents =
                      sport.getCategoryId() == MainTier2Sports.GOLF.getCategoryId()
                          ? ((SiteServeServiceImpl) siteServeService)
                              .anyUpcomingEventsExistsForGolf(sport)
                          : siteServeService.anyLiveOrUpcomingEventsExists(sport);

                  adjustHasEventsValue(tab, hasEvents);
                  return sport;
                }));
  }
}
