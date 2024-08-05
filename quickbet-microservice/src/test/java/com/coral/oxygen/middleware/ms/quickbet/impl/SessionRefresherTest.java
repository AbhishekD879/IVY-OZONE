package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;

/**
 * @author volodymyr.masliy
 */
class SessionRefresherTest {
  @Test
  void testDelayAmount() {
    SessionRefresher<String> sessionRefresher =
        new SessionRefresher<>(s -> true, new SessionRefresher.TimeAmount(10, TimeUnit.SECONDS));
    ScheduledFuture scheduledFuture = sessionRefresher.registerSession("123");
    long delay = scheduledFuture.getDelay(TimeUnit.SECONDS);
    assertThat(delay).isLessThanOrEqualTo(5L).isGreaterThanOrEqualTo(3L);
  }

  @Test
  void testTaskIsCancelledOnException() throws InterruptedException {
    SessionRefresher<String> sessionRefresher =
        new SessionRefresher<>(s -> false, new SessionRefresher.TimeAmount(10, TimeUnit.SECONDS));
    sessionRefresher.setDelayCalculationStrategy(
        ttl -> new SessionRefresher.TimeAmount(1, TimeUnit.SECONDS));
    ScheduledFuture scheduledFuture = sessionRefresher.registerSession("123");
    assertThatThrownBy(() -> scheduledFuture.get(3, TimeUnit.SECONDS))
        .isInstanceOf(ExecutionException.class)
        .hasMessageContaining("Failed to refresh session because it doesn't exist");
  }

  @Test
  void testTaskIsNotDoneAfterFirstTry() throws InterruptedException {
    SessionRefresher<String> sessionRefresher =
        new SessionRefresher<>(s -> true, new SessionRefresher.TimeAmount(10, TimeUnit.SECONDS));
    sessionRefresher.setDelayCalculationStrategy(
        ttl -> new SessionRefresher.TimeAmount(1, TimeUnit.SECONDS));
    ScheduledFuture scheduledFuture = sessionRefresher.registerSession("123");
    TimeUnit.SECONDS.sleep(3);
    assertThat(scheduledFuture.isDone()).isFalse();
  }
}
