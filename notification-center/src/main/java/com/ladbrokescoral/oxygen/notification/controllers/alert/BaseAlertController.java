package com.ladbrokescoral.oxygen.notification.controllers.alert;

import static org.springframework.http.ResponseEntity.accepted;
import static org.springframework.http.ResponseEntity.status;

import com.ladbrokescoral.oxygen.notification.entities.BaseSubscription;
import com.ladbrokescoral.oxygen.notification.entities.ErrorResponse;
import com.ladbrokescoral.oxygen.notification.entities.ErrorResponse.ErrorResponseBuilder;
import com.ladbrokescoral.oxygen.notification.services.ConsumeEventException;
import com.ladbrokescoral.oxygen.notification.services.alert.AlertService;
import com.newrelic.api.agent.NewRelic;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/** Handles subscription on Win Alerts. The abstraction is unnecessary, should be simplified. */
@Slf4j
public abstract class BaseAlertController {

  private AlertService alertService;

  public BaseAlertController(AlertService alertService) {
    this.alertService = alertService;
  }

  ResponseEntity<?> subscribe(final BaseSubscription request) {
    logger.info("Request: " + request.toString());
    try {
      BaseSubscription response = alertService.save(request);
      logger.info("Response: " + response.toString());
      return accepted().body(response);
    } catch (ConsumeEventException e) {
      logger.error(e.getMessage(), e);
      NewRelic.noticeError(e);
      HttpStatus status = HttpStatus.INTERNAL_SERVER_ERROR;
      ErrorResponseBuilder builder = ErrorResponse.builder();
      builder.errorMessage(e.getMessage());
      builder.status(status);
      return status(status).body(builder.build());
    }
  }
}
