package com.ladbrokescoral.oxygen.notification.controllers.alert;

import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.services.alert.AlertService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/** This is unused, to be removed. */
@Slf4j
@RestController
public class RacingController extends BaseAlertController {

  @Autowired
  public RacingController(@Qualifier("RacingAlertService") AlertService alertService) {
    super(alertService);
  }

  @PutMapping(path = "racing/subscription", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<?> subscribeOnWinAlerts(@RequestBody final Item request) {
    return subscribe(request);
  }

  @InitBinder
  public void populateRequest(WebDataBinder binder) {
    binder.setDisallowedFields(binder.getDisallowedFields());
  }
}
