package com.oxygen.publisher.sportsfeatured.service;

import com.oxygen.health.api.ReloadableService;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.stream.Collectors;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RequiredArgsConstructor
public class SportsPageIdRegistration implements ReloadableService {
  private AtomicBoolean isOnService = new AtomicBoolean();
  private final FeaturedService featuredService;
  private final SportIdFilter sportIdFilter;

  @Getter private final SportsCachedData sportsCachedData;

  @Override
  public void start() {
    this.isOnService.set(true);
    featuredService.getSportPages(
        (List<String> pageIds) -> {
          Map<String, PageRawIndex> sportPageMap =
              pageIds.stream()
                  .filter(sportIdFilter::isSupportedPageType)
                  .collect(Collectors.toMap(pageValue -> pageValue, PageRawIndex::fromPageId));
          sportsCachedData.insertSportPageData(sportPageMap);
        });
  }

  @Override
  public void evict() {
    this.isOnService.set(false);
  }

  @Override
  public boolean isHealthy() {
    return isOnService.get();
  }

  @Override
  public void onFail(Exception ex) {
    this.isOnService.set(false);
    log.error("WS sportId registration failed.", ex);
  }
}
