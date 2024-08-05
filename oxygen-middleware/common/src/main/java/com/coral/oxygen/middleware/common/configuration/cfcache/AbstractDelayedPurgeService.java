package com.coral.oxygen.middleware.common.configuration.cfcache;

import com.newrelic.api.agent.NewRelic;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang.StringUtils;

@Slf4j
public abstract class AbstractDelayedPurgeService implements CachePurgeService {

  private final BlockingQueue<CCUItem> queue;
  private final Integer maxQueueSize;
  private final ScheduledExecutorService executor;
  private final Integer purgeItemsMaxLimit;

  protected AbstractDelayedPurgeService(
      Integer purgeItemsCapacity,
      Integer initialDelaySeconds,
      Integer fixedDelaySeconds,
      Integer purgeItemsMaxLimit) {
    queue = new ArrayBlockingQueue<>(purgeItemsCapacity);
    maxQueueSize = purgeItemsCapacity;
    this.purgeItemsMaxLimit = purgeItemsMaxLimit;
    log.info("Creating scheduled cache client for items purge");
    executor = Executors.newSingleThreadScheduledExecutor();
    executor.scheduleAtFixedRate(
        this::purgeCache, initialDelaySeconds, fixedDelaySeconds, TimeUnit.SECONDS);
  }

  private void purgeCache() {
    try {
      List<CCUItem> purgeItems = new ArrayList<>(maxQueueSize);
      queue.drainTo(purgeItems, purgeItemsMaxLimit);
      if (!purgeItems.isEmpty()) {
        purgeItems.stream()
            .collect(Collectors.groupingBy(CCUItem::getBrand))
            .forEach(
                (brand, items) ->
                    doPurgeItems(items).stream()
                        .filter(Objects::nonNull)
                        .filter(Optional::isPresent)
                        .forEach(r -> logSuccessStatus(brand, r.get())));
      }
    } catch (Exception e) {
      log.error("Can't force purge content", e);
      NewRelic.noticeError(e);
    }
  }

  protected abstract List<Optional<InvalidateCacheResult>> doPurgeItems(List<CCUItem> purgeItems);

  private void logSuccessStatus(String brand, InvalidateCacheResult result) {
    log.info(
        "Purge CF Cache {} :: {} :: {} :: {} :: {} :: {}",
        brand,
        Instant.now(),
        result.getResponseCode(),
        result.getMessage(),
        result.getServiceType(),
        StringUtils.join(result.getInvalidatedItems(), ", "));
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
