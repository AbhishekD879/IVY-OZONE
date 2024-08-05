package com.ladbrokescoral.oxygen.notification.services;

import com.google.gson.Gson;
import com.ladbrokescoral.oxyegn.test.utils.Utils;
import com.ladbrokescoral.oxygen.notification.entities.bet.Betslip;
import com.ladbrokescoral.oxygen.notification.services.alert.WinAlertMessageHandler;
import java.io.IOException;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class KafkaListenerServiceTest {

  @Mock private NotificationsMessageHandler notificationsMessageHandler;

  @Mock private WinAlertMessageHandler winAlertMessageHandler;

  private Gson gson = new Gson();

  @Test
  public void listenWinAlert() throws IOException {
    KafkaListenerService service =
        new KafkaListenerService(notificationsMessageHandler, winAlertMessageHandler, gson);
    service.listenWinAlert(
        Utils.fromResource("bet/betslip.json", this.getClass().getClassLoader()));
    Mockito.verify(winAlertMessageHandler, Mockito.times(1)).handleBetslip(Mockito.any());
  }

  @Test
  public void listenWinAlertInvalidJson() throws IOException {
    KafkaListenerService service =
        new KafkaListenerService(notificationsMessageHandler, winAlertMessageHandler, gson);
    service.listenWinAlert(Utils.fromResource("invalid.json", this.getClass().getClassLoader()));
    Betslip betslip = new Betslip();
    betslip.setUsername("test");
    Mockito.verify(winAlertMessageHandler, Mockito.times(1)).handleBetslip(Mockito.eq(betslip));
  }
}
