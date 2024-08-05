package com.coral.oxygen.middleware.configuration;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.cms.api.HealthStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.boot.actuate.health.Status;
import org.springframework.context.annotation.Configuration;

/** Created by llegkyy on 03.10.17. */
@Configuration
public class CmsServiceHealthIndicator implements HealthIndicator {
  private CmsService cmsService;

  @Autowired
  public CmsServiceHealthIndicator(CmsService cmsService) {
    this.cmsService = cmsService;
  }

  @Override
  public Health health() {
    if (cmsService.getHealthStatus().equals(HealthStatus.OK)) {
      return Health.status(Status.UP).build();
    } else {
      return Health.status(Status.OUT_OF_SERVICE).build();
    }
  }
}
