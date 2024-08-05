package com.ladbrokescoral.oxygen.notification.controllers.alert;

import com.ladbrokescoral.oxygen.notification.services.ConsumeEventException;
import com.ladbrokescoral.oxygen.notification.services.alert.AlertService;
import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;
import org.springframework.web.bind.WebDataBinder;

public class RacingControllerTest {
  @Test
  public void binderTest() {
    AlertService alertService = Mockito.mock(AlertService.class);
    Mockito.when(alertService.save(Mockito.any()))
        .thenThrow(new ConsumeEventException("test error"));
    RacingController racingController = new RacingController(alertService);
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    racingController.populateRequest(webDataBinder);
    Assert.assertNotNull(racingController);
  }
}
