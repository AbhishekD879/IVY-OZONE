package com.coral.oxygen.edp.tracking;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class ExecutorUpdateScheduler implements UpdateScheduler {

  private static final int TIME_WINDOW_MILLISECONDS = 1000; // avoid scheduling on the same second

  private Tracker tracker;
  private final ScheduledExecutorService executorService;
  private ScheduledFuture latestFuture;

  public ExecutorUpdateScheduler() {
    executorService = Executors.newSingleThreadScheduledExecutor();
  }

  @Override
  public void setTracker(Tracker tracker) {
    this.tracker = tracker;
  }

  @Override
  public void schedule(long milliseconds) {
    if (!willScheduleAtSameTime(milliseconds, latestFuture)) {
      log.info("scheduled next call in {} sec", milliseconds / 1000);
      latestFuture =
          executorService.schedule(
              () -> {
                log.info(
                    "Performing scheduled data refresh for tracker: {}",
                    tracker.getClass().getSimpleName());
                tracker.refreshData();
                latestFuture = null;
              },
              milliseconds,
              TimeUnit.MILLISECONDS);
    } else {
      log.info("not scheduled in the same time frame");
    }
  }

  private boolean willScheduleAtSameTime(long milliseconds, ScheduledFuture future) {
    if (future == null) {
      return false;
    }
    long delay = future.getDelay(TimeUnit.MILLISECONDS);
    return milliseconds > delay - TIME_WINDOW_MILLISECONDS
        || milliseconds < delay + TIME_WINDOW_MILLISECONDS;
  }
}
