package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.newrelic.api.agent.NewRelic;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import java.util.function.Predicate;
import java.util.function.UnaryOperator;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Periodically runs refresh action on registered sessions
 *
 * @author volodymyr.masliy
 */
public final class SessionRefresher<T> {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Predicate<T> refreshAction;
  private ScheduledExecutorService scheduledExecutor;
  private UnaryOperator<TimeAmount> delayCalculationStrategy =
      SessionRefresher::defaultDelayCalculationStrategy;
  private TimeAmount sessionTtl;

  /**
   * @param refreshAction - function that's supposed to refresh session
   * @param sessionTtl - session's expiration time
   */
  public SessionRefresher(Predicate<T> refreshAction, TimeAmount sessionTtl) {
    this.refreshAction = refreshAction;
    this.sessionTtl = sessionTtl;
    this.scheduledExecutor = Executors.newScheduledThreadPool(5);
  }

  private static TimeAmount defaultDelayCalculationStrategy(TimeAmount ttl) {
    return new TimeAmount(ttl.getDelay() / 2, ttl.getTimeUnit());
  }

  public ScheduledFuture registerSession(T sessionId) {
    TimeAmount delay = calculateDelayBeforeRefreshing();
    return this.scheduledExecutor.scheduleWithFixedDelay(
        new RefreshTask(refreshAction, sessionId),
        delay.getDelay(),
        delay.getDelay(),
        delay.getTimeUnit());
  }

  private TimeAmount calculateDelayBeforeRefreshing() {
    return delayCalculationStrategy.apply(sessionTtl);
  }

  public void setDelayCalculationStrategy(UnaryOperator<TimeAmount> delayCalculationStrategy) {
    this.delayCalculationStrategy = delayCalculationStrategy;
  }

  // Wraps refresh action function to capture its result
  private class RefreshTask implements Runnable {
    private final Predicate<T> refreshAction;
    private final T sessionId;

    RefreshTask(Predicate<T> refreshAction, T sessionId) {
      this.refreshAction = refreshAction;
      this.sessionId = sessionId;
    }

    @Override
    public void run() {
      try {
        boolean isRefreshed = refreshAction.test(sessionId);
        if (!isRefreshed) {
          ASYNC_LOGGER.error("Error refreshing session: {}", sessionId);
          throw new IllegalStateException("Failed to refresh session because it doesn't exist");
        }
      } catch (Exception e) {
        ASYNC_LOGGER.error("Error executing refresh procedure");
        NewRelic.noticeError(e);
        throw new IllegalStateException(e);
      }
    }
  }

  public static class TimeAmount {
    private long delay;
    private TimeUnit timeUnit;

    public TimeAmount(long delay, TimeUnit timeUnit) {
      this.delay = delay;
      this.timeUnit = timeUnit;
    }

    public long getDelay() {
      return delay;
    }

    public TimeUnit getTimeUnit() {
      return timeUnit;
    }
  }
}
