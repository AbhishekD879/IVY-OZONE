package com.ladbrokescoral.oxygen.notification.controllers.alert;

import com.ladbrokescoral.oxygen.notification.entities.WinAlertSubscriptionRequest;
import com.ladbrokescoral.oxygen.notification.entities.WinalertStatus;
import com.ladbrokescoral.oxygen.notification.services.alert.AlertService;
import com.ladbrokescoral.oxygen.notification.services.alert.WinAlertService;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/** Saves subs */
@Slf4j
@RestController
public class WinAlertController extends BaseAlertController {
  private WinAlertService winAlertService;

  @Autowired
  public WinAlertController(
      @Qualifier("WinAlertService") AlertService alertService, WinAlertService winAlertService) {
    super(alertService);
    this.winAlertService = winAlertService;
  }

  @PutMapping(path = "winalert/subscription", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<?> subscribeOnWinAlerts(
      @RequestBody final WinAlertSubscriptionRequest request) {
    return subscribe(request);
  }

  @PostMapping(path = "winalert/status", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<List<String>> getWinalertSubscriptionstatus(
      @RequestBody final WinalertStatus request) {
    return winAlertService.getWinalertSubscriptionstatus(request);
  }

  @PostMapping(path = "winalert/delete", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity<Boolean> deleteWinalertSubscription(
      @RequestBody final WinalertStatus request) {
    return winAlertService.deleteWinalertSubscription(request);
  }

  @InitBinder
  public void populateRequest(WebDataBinder binder) {
    binder.setDisallowedFields(binder.getDisallowedFields());
  }
}
