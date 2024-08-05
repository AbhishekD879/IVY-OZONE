package com.ladbrokescoral.oxygen.cms.api.service.sporttab.checker;

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TierCategoriesCache;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;

@Slf4j
@AllArgsConstructor
public abstract class EventsChecker {
  private final ScheduledTaskExecutor scheduledTaskExecutor;
  protected final SportTabService sportTabService;
  protected final TierCategoriesCache tierCategoriesCache;

  @Scheduled(initialDelay = 0L, fixedDelay = 30000)
  public void checkForEvents() {
    scheduledTaskExecutor.execute(
        () -> {
          try {
            log.debug("Starting to schedule {} with params", this.getClass().getSimpleName());
            tierCategoriesCache.refreshCategoryIdsCache();
            doCheck();
          } catch (Exception e) {
            log.error("Error in eventChecker {}, {}", this.getClass(), e.getMessage());
          }
        });
  }

  protected abstract void doCheck();

  protected void adjustHasEventsValue(SportTab tab, boolean hasEvents) {
    if (tab.isHasEvents() != hasEvents) {
      log.info(
          "{} tab for brand {} was saved. hasEvents value changed from {} to {}",
          tab.getName(),
          tab.getBrand(),
          tab.isHasEvents(),
          hasEvents);
      tab.setHasEvents(hasEvents);
      sportTabService.save(tab);
    }
  }

  protected Set<Integer> extractSportIds(List<SportTab> tabs) {
    return tabs.stream().map(SportTab::getSportId).collect(Collectors.toSet());
  }
}
