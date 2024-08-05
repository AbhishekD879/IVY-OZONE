package com.ladbrokescoral.oxygen.notification.controllers.alert;

import com.ladbrokescoral.oxygen.notification.entities.ErrorResponse;
import com.ladbrokescoral.oxygen.notification.entities.WinAlertSubscriptionRequest;
import com.ladbrokescoral.oxygen.notification.entities.WinalertStatus;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import com.ladbrokescoral.oxygen.notification.services.ConsumeEventException;
import com.ladbrokescoral.oxygen.notification.services.alert.AlertService;
import com.ladbrokescoral.oxygen.notification.services.alert.WinAlertService;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.WebDataBinder;

public class WinAlertControllerTest {

  @Mock private RedisTemplate<String, WinAlertDTO> template;
  @Mock RedisTemplate<String, List<String>> winAlertSubScriptionTemplates;

  @Test
  public void subscribeOnWinAlerts() {
    AlertService alertService = Mockito.mock(AlertService.class);
    WinAlertService winAlertService = Mockito.mock(WinAlertService.class);
    Mockito.when(alertService.save(Mockito.any()))
        .thenThrow(new ConsumeEventException("test error"));
    WinAlertController controller = new WinAlertController(alertService, winAlertService);
    WinAlertSubscriptionRequest request = new WinAlertSubscriptionRequest();
    ResponseEntity<ErrorResponse> responseEntity =
        (ResponseEntity<ErrorResponse>) controller.subscribeOnWinAlerts(request);
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    controller.populateRequest(webDataBinder);
    Assert.assertNotNull(responseEntity);
    Assert.assertNotNull(responseEntity.getBody());
    Assert.assertEquals("test error", responseEntity.getBody().getErrorMessage());
  }

  @Test
  public void getWinalertSubscriptionstatus() {
    AlertService alertService = Mockito.mock(AlertService.class);
    WinAlertService winAlertService = Mockito.mock(WinAlertService.class);
    Mockito.when(
            winAlertService.getWinalertSubscriptionstatus(
                new WinalertStatus("test", "test", "test", "test")))
        .thenReturn(new ResponseEntity<>(HttpStatus.ACCEPTED));
    WinAlertController controller = new WinAlertController(alertService, winAlertService);
    WinalertStatus request = new WinalertStatus("test", "test", "test", "test");
    ResponseEntity<List<String>> responseEntity = controller.getWinalertSubscriptionstatus(request);
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    controller.populateRequest(webDataBinder);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalertSubscription() {
    AlertService alertService = Mockito.mock(AlertService.class);
    WinAlertService winAlertService = Mockito.mock(WinAlertService.class);
    Mockito.when(
            winAlertService.deleteWinalertSubscription(
                new WinalertStatus("test", "test", "test", "test")))
        .thenReturn(new ResponseEntity<>(HttpStatus.ACCEPTED));
    WinAlertController controller = new WinAlertController(alertService, winAlertService);
    WinalertStatus request = new WinalertStatus("test", "test", "test", "test");
    ResponseEntity<Boolean> responseEntity = controller.deleteWinalertSubscription(request);
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    controller.populateRequest(webDataBinder);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }
}
