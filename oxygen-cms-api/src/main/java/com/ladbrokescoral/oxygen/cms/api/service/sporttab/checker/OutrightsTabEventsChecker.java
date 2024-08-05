package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

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
public class OutrightsTabEventsChecker extends EventsChecker {

  private final SiteServeService siteServeService;
  private final String brand;

  public OutrightsTabEventsChecker(
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
    List<SportTab> outrightTabs =
        sportTabService.findAllForCheckingEvents(brand, SportTabNames.OUTRIGHTS).stream()
            .filter(tab -> belongsToTier(tab, SportTier.TIER_2))
            .collect(Collectors.toList());

    Set<Integer> categoriesWithOutrights =
        siteServeService.filterByOutrightEvents(brand, extractSportIds(outrightTabs));
    log.trace("Brand: {}. Categories with Outrights events: {}", brand, categoriesWithOutrights);

    outrightTabs.forEach(
        tab -> {
          boolean hasEvents = categoriesWithOutrights.contains(tab.getSportId());
          adjustHasEventsValue(tab, hasEvents);
        });
  }

  private boolean belongsToTier(SportTab tab, SportTier tier) {
    return tierCategoriesCache.getCategoryIds(tab.getBrand(), tier).contains(tab.getSportId());
  }
}
