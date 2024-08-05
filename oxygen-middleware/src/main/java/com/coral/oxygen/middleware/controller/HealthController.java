package com.coral.oxygen.middleware.controller;

import com.coral.oxygen.middleware.common.imdg.DistributedInstance;
import com.coral.oxygen.middleware.component.MiddlewareHealthIndicator;
import com.coral.oxygen.middleware.configuration.CmsServiceHealthIndicator;
import com.coral.oxygen.middleware.configuration.SiteServHealthIndicator;
import com.newrelic.api.agent.NewRelic;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.health.Status;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by llegkyy on 03.10.17. */
@Slf4j
@RestController
public class HealthController {

  private static final String CMS_AND_SS_OUT_OF_SERVICE =
      "CMS and SiteServer are out of service, marking the Middleware as out of service!";
  private static final String DISTRIBUTED_INSTANCE_OUT_OF_SERVICE =
      "%s is out of service. Stopping the Middleware service!";
  private static final String SCHEDULER_THREAD_MIGHT_BE_DEAD =
      "Scheduler thread might be dead, marking the Middleware as out of service!";

  private CmsServiceHealthIndicator cmsServiceHealthIndicator;
  private SiteServHealthIndicator siteServHealthIndicator;
  private MiddlewareHealthIndicator middlewareHealthIndicator;
  private DistributedInstance distributedInstance;

  @Autowired
  public HealthController(
      CmsServiceHealthIndicator cmsServiceHealthIndicator,
      SiteServHealthIndicator siteServHealthIndicator,
      DistributedInstance distributedInstance,
      MiddlewareHealthIndicator middlewareHealthIndicator) {
    this.cmsServiceHealthIndicator = cmsServiceHealthIndicator;
    this.siteServHealthIndicator = siteServHealthIndicator;
    this.distributedInstance = distributedInstance;
    this.middlewareHealthIndicator = middlewareHealthIndicator;
  }

  @GetMapping("/health")
  public ResponseEntity<String> getHealth() {
    HttpStatus httpStatus = HttpStatus.OK;
    Status cmsStatus = cmsServiceHealthIndicator.health().getStatus();
    Status siteServeStatus = siteServHealthIndicator.health().getStatus();
    Status middlewareStatus = middlewareHealthIndicator.health().getStatus();
    Status distributedInstanceStatus =
        distributedInstance.getHealthIndicator().health().getStatus();
    if (cmsStatus.equals(Status.OUT_OF_SERVICE) && siteServeStatus.equals(Status.OUT_OF_SERVICE)) {
      NewRelic.noticeError(CMS_AND_SS_OUT_OF_SERVICE);
      log.error(CMS_AND_SS_OUT_OF_SERVICE);
    }
    if (distributedInstanceStatus.equals(Status.OUT_OF_SERVICE)) {
      String message =
          distributedInstanceOutOfServiceMessage(distributedInstance.getProviderName());
      NewRelic.noticeError(message);
      log.error(message);
      httpStatus = HttpStatus.SERVICE_UNAVAILABLE;
    }

    if (middlewareStatus.equals(Status.OUT_OF_SERVICE)) {
      NewRelic.noticeError(SCHEDULER_THREAD_MIGHT_BE_DEAD);
      log.error(SCHEDULER_THREAD_MIGHT_BE_DEAD);
      httpStatus = HttpStatus.SERVICE_UNAVAILABLE;
    }

    return new ResponseEntity<>("Health check status", httpStatus);
  }

  private String distributedInstanceOutOfServiceMessage(String distributedProviderName) {
    return String.format(DISTRIBUTED_INSTANCE_OUT_OF_SERVICE, distributedProviderName);
  }
}
