package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SpecialsChecker extends EventsChecker {

  private final SiteServeService siteServeService;
  private final String brand;

  public SpecialsChecker(
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
    Set<Integer> sportsId = new HashSet<>();
    sportsId.addAll(tierCategoriesCache.getCategoryIds(brand, SportTier.TIER_1));
    sportsId.addAll(tierCategoriesCache.getCategoryIds(brand, SportTier.TIER_2));

    sportsId.forEach(
        categoryId -> {
          List<Event> sportSpecials = siteServeService.getSportSpecials(brand, categoryId);

          sportTabService.updateHasEvents(
              brand, categoryId, SportTabNames.SPECIALS, !sportSpecials.isEmpty());
        });
  }
}
