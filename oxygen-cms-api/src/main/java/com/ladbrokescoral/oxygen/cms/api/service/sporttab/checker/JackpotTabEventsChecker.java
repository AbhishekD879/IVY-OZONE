package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabNames;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class JackpotTabEventsChecker extends EventsChecker {

  private final SiteServeService siteServeService;

  public JackpotTabEventsChecker(
      ScheduledTaskExecutor scheduledTaskExecutor,
      SiteServeService siteServeService,
      SportTabService sportTabService,
      TierCategoriesCache tierCategoriesCache) {
    super(scheduledTaskExecutor, sportTabService, tierCategoriesCache);
    this.siteServeService = siteServeService;
  }

  @Override
  protected void doCheck() {
    List<SportTab> jackpotTabs =
        sportTabService.findWithEnabledCheckEvents(SportTabNames.JACKPOT.nameLowerCase());

    jackpotTabs.forEach(
        tab -> {
          boolean hasEvents = siteServeService.hasSiteServeJackpotEvents(tab.getBrand());
          adjustHasEventsValue(tab, hasEvents);
        });
  }
}
