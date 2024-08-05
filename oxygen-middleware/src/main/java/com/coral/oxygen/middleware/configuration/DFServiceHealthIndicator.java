package com.coral.oxygen.middleware.configuration;

import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.df.api.HealthStatus;
import java.util.Collections;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.boot.actuate.health.Status;
import org.springframework.stereotype.Component;

/** Created by llegkyy on 03.10.17. */
@Component
public class DFServiceHealthIndicator implements HealthIndicator {

  private DFService service;
  private int categoryId;

  @Autowired
  public DFServiceHealthIndicator(
      DFService service, @Value("${df.category.horse}") int categoryId) {
    this.service = service;
    this.categoryId = categoryId;
  }

  @Override
  public Health health() {
    service.getRaceEvents(categoryId, Collections.singletonList(123456L));
    if (service.getHealthStatus().equals(HealthStatus.OK)) {
      return Health.status(Status.UP).build();
    } else {
      return Health.status(Status.OUT_OF_SERVICE).build();
    }
  }
}
