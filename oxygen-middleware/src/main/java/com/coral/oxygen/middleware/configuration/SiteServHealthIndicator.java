package com.coral.oxygen.middleware.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.SiteServerManage;
import com.egalacoral.spark.siteserver.model.HealthCheck;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.boot.actuate.health.Status;
import org.springframework.context.annotation.Configuration;

/** Created by llegkyy on 29.09.17. */
@Slf4j
@Configuration
public class SiteServHealthIndicator implements HealthIndicator {

  private SiteServerManage siteServerManage;

  @Autowired
  public SiteServHealthIndicator(SiteServerApi siteServerApi) {
    if (siteServerApi instanceof SiteServerManage) {
      this.siteServerManage = (SiteServerManage) siteServerApi;
    } else {
      throw new IllegalStateException(
          "The siteServerApi should implement SiteServerManage interface.");
    }
  }

  @Override
  public Health health() {
    Health status = Health.status(Status.OUT_OF_SERVICE).build();
    Optional<HealthCheck> healthCheck = Optional.empty();
    try {
      healthCheck = siteServerManage.getHealthCheck();
    } catch (Exception e) {
      log.error("Enable to call siteserv health page", e);
    }
    if (healthCheck.isPresent() && healthCheck.get().getStatus().equals("OK")) {
      status = Health.status(Status.UP).build();
    }
    return status;
  }
}
