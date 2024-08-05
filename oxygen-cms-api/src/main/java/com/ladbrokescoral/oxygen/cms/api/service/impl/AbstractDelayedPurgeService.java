package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.CCUItem;
import com.ladbrokescoral.oxygen.cms.api.entity.Dashboard;
import com.ladbrokescoral.oxygen.cms.api.service.DashboardService;
import com.newrelic.api.agent.NewRelic;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

@Slf4j
public abstract class AbstractDelayedPurgeService implements CachePurgeService {

  private final BlockingQueue<CCUItem> queue;
  private final DashboardService dashboardService;
  private final Integer maxQueueSize;
  private final ScheduledExecutorService executor;

  public AbstractDelayedPurgeService(
      DashboardService service,
      Integer purgeItemsCapacity,
      Integer initialDelaySeconds,
      Integer fixedDelaySeconds) {
    dashboardService = service;
    queue = new ArrayBlockingQueue<>(purgeItemsCapacity);
    maxQueueSize = purgeItemsCapacity;
    log.info("Creating scheduled cache client for items purge");
    executor = Executors.newSingleThreadScheduledExecutor();
    executor.scheduleAtFixedRate(
        this::purgeCache, initialDelaySeconds, fixedDelaySeconds, TimeUnit.SECONDS);
  }

  private void purgeCache() {
    try {
      List<CCUItem> purgeItems = new ArrayList<>(maxQueueSize);
      queue.drainTo(purgeItems);
      if (!purgeItems.isEmpty()) {
        purgeItems.stream()
            .collect(Collectors.groupingBy(CCUItem::getBrand))
            .forEach(
                (brand, items) ->
                    doPurgeItems(items).stream()
                        .filter(Objects::nonNull)
                        .filter(Optional::isPresent)
                        .forEach(r -> showSuccessStatusAtDashboard(brand, r.get())));
      }
    } catch (Exception e) {
      log.error("Can't force purge content", e);
      NewRelic.noticeError(e);
    }
  }

  protected abstract List<Optional<InvalidateCacheResult>> doPurgeItems(List<CCUItem> purgeItems);

  private void showSuccessStatusAtDashboard(String brand, InvalidateCacheResult result) {
    Dashboard dashboard =
        Dashboard.builder()
            .brand(brand)
            .currentTime(Instant.now())
            .status(result.getResponseCode())
            .message(result.getMessage())
            .type(result.getServiceType())
            .domains(StringUtils.join(result.getInvalidatedItems(), ", "))
            .build();
    dashboardService.save(dashboard);
  }

  protected void delayPurge(CCUItem purgeItem) {
    queue.add(purgeItem);
  }

  @Override
  public void shutdown() {
    queue.clear();
    executor.shutdownNow();
  }
}
