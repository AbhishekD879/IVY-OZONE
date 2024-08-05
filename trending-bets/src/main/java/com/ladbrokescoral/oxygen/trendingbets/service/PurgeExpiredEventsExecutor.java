package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularBets;
import java.util.concurrent.*;
import java.util.stream.IntStream;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.concurrent.CustomizableThreadFactory;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class PurgeExpiredEventsExecutor {
  private static final double TEN_PERCENT = 0.1;

  private final ExecutorService executor;
  private final Integer queueSize;

  private static final Integer MAX_THREADS = 10;

  @Autowired
  public PurgeExpiredEventsExecutor(
      @Value("${trendingbets.max.queue.capacity:500}") Integer queueSize) {
    executor =
        Executors.newFixedThreadPool(
            MAX_THREADS, new CustomizableThreadFactory("purge-Events-Expired-"));
    this.queueSize = queueSize;
  }

  @PostConstruct
  public void runUploadWorkers() {
    if (!executor.isShutdown()) {
      IntStream.range(0, 1).forEach(w -> executor.execute(this::deliverIndefinitely));
    }
  }

  @PreDestroy
  public void shutdown() {
    executor.shutdownNow();
  }

  private void deliverIndefinitely() {
    while (!Thread.currentThread().isInterrupted()) {
      try {
        TrendingBetsContext.getItemToPurge()
            .forEach(
                event -> TrendingBetsContext.cleanSelections(event, PopularBets.PERSONALIZED_BETS));
        monitorQueueCapacityEnding();
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        runUploadWorkers();
      } catch (Exception e) {
        log.error("Error UnSubscribing the Events {}", e);
      }
    }
  }

  private void monitorQueueCapacityEnding() {
    if (TrendingBetsContext.getUploadPendingQueue().remainingCapacity() < TEN_PERCENT * queueSize) {
      log.warn(
          "Pending queue is almost full, remaining capacity; {}",
          TrendingBetsContext.getUploadPendingQueue().remainingCapacity());
    }
  }
}
