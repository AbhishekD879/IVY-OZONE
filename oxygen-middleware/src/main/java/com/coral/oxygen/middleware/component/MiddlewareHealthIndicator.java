package com.coral.oxygen.middleware.component;

import com.coral.oxygen.middleware.scheduler.ConsumeScheduledTask;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Component;

@Component
@DependsOn("ApplicationConfiguration")
public class MiddlewareHealthIndicator implements HealthIndicator {

  private ConsumeScheduledTask consumeScheduledTask;
  private int loyalPeriodSeconds;

  @Autowired
  public MiddlewareHealthIndicator(
      ConsumeScheduledTask consumeScheduledTask,
      @Value("${health.loyalPeriodSeconds}") int loyalPeriodSeconds) {
    this.consumeScheduledTask = consumeScheduledTask;
    this.loyalPeriodSeconds = loyalPeriodSeconds;
  }

  @Override
  public Health health() {
    return isLoyalPeriodNotExceeded() ? Health.up().build() : Health.outOfService().build();
  }

  private boolean isLoyalPeriodNotExceeded() {
    long lastRun = consumeScheduledTask.getLastTimeLaunched();
    long current = System.currentTimeMillis();
    return (current - lastRun) <= (loyalPeriodSeconds * 1000);
  }
}
