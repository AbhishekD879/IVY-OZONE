package com.ladbrokescoral.oxygen.notification.services.alert;

import static com.ladbrokescoral.oxyegn.test.utils.Utils.fromResource;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.bet.Betslip;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import com.ladbrokescoral.oxygen.notification.services.SiteServerApiService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

@RunWith(MockitoJUnitRunner.class)
public class WinAlertMessageHandlerTest {

  private static final Gson GSON = new GsonBuilder().create();
  private static final String MOCK_KEY =
      RedisKey.forWinAlert("O/0229182/0000027", Platform.ANDROID.getName());
  String WinlalertSubscriptionKey =
      "Johnny English" + "jdsBKBNr433JSDIfsdjhfs4f3U932di2" + "android";

  private static final String MOCK_TOKEN = "jdsBKBNr433JSDIfsdjhfs4f3U932di2";
  private static final String MOCK_OUTCOME_ID = "522885001";
  private static final String MOCK_OUTCOME_NAME = "Some bet";
  private static final String WELL_FORMATTED_MESSAGE =
      "Congratulations Johnny English, your bet on Some bet has won and your account has been credited with GBP 2.60";
  private static final String NOTIFICATION_TITLE = "You have a winner!";
  private static final String DEEP_LINK = "open-bets";

  private String winBetslip;
  private String betslip;

  private WinAlertMessageHandler winAlertMessageHandler;

  @Mock private RedisTemplate<String, WinAlertDTO> template;
  @Mock RedisTemplate<String, List<String>> winAlertSubScriptionTemplates;

  @Mock private ValueOperations<String, WinAlertDTO> operations;
  @Mock private ValueOperations<String, List<String>> winAlertOperations;

  @Mock private NotificationsFactory notificationsFactory;

  @Mock private SiteServerApiService siteServerApiService;

  @Before
  public void setUp() throws IOException {
    MockitoAnnotations.initMocks(this);
    Type stringMapType = new TypeToken<Map<String, String>>() {}.getType();
    Map<String, String> betTypes =
        GSON.fromJson(
            new InputStreamReader(
                Objects.requireNonNull(
                    this.getClass()
                        .getClassLoader()
                        .getResourceAsStream("map/bet_types_map.json"))),
            stringMapType);

    WinAlertDTO dto =
        WinAlertDTO.builder()
            .betId("O/0229182/0000027")
            .platform("android")
            .token("jdsBKBNr433JSDIfsdjhfs4f3U932di2")
            .userName("Johnny English")
            .build();

    winAlertMessageHandler =
        new WinAlertMessageHandlerImpl(
            DEEP_LINK,
            template,
            notificationsFactory,
            betTypes,
            siteServerApiService,
            winAlertSubScriptionTemplates);

    winBetslip = fromResource("bet/betslip_win.json", this.getClass().getClassLoader());
    betslip = fromResource("bet/betslip.json", this.getClass().getClassLoader());

    Mockito.when(template.opsForValue()).thenReturn(operations);
    Mockito.when(operations.get(MOCK_KEY)).thenReturn(dto);
    Mockito.when(winAlertSubScriptionTemplates.opsForValue()).thenReturn(winAlertOperations);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Arrays.asList("O/0229182/0000027"));
    Mockito.when(notificationsFactory.notify(getDevice(), getPayload())).thenReturn(true);

    Mockito.when(siteServerApiService.getOutcomeName(MOCK_OUTCOME_ID))
        .thenReturn(MOCK_OUTCOME_NAME);
  }

  @Test
  public void testServiceSendsNotificationOnWin() {
    winAlertMessageHandler.handleBetslip(GSON.fromJson(winBetslip, Betslip.class));

    Mockito.verify(notificationsFactory).notify(getDevice(), getPayload());

    Mockito.verify(template).delete(MOCK_KEY);
  }

  @Test
  public void testServiceSendsNotificationOnWinNoSubData() {
    Mockito.when(winAlertSubScriptionTemplates.opsForValue()).thenReturn(winAlertOperations);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Arrays.asList("O/0229182/0000028"));
    winAlertMessageHandler.handleBetslip(GSON.fromJson(winBetslip, Betslip.class));

    Mockito.verify(notificationsFactory).notify(getDevice(), getPayload());

    Mockito.verify(template).delete(MOCK_KEY);
  }

  @Test
  public void testServiceSendsNotificationOnWinNullSubData() {
    Mockito.when(winAlertSubScriptionTemplates.opsForValue()).thenReturn(winAlertOperations);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey)).thenReturn(null);
    winAlertMessageHandler.handleBetslip(GSON.fromJson(winBetslip, Betslip.class));

    Mockito.verify(notificationsFactory).notify(getDevice(), getPayload());

    Mockito.verify(template).delete(MOCK_KEY);
  }

  @Test
  public void testServiceDoesNotSendNotification() {

    winAlertMessageHandler.handleBetslip(GSON.fromJson(betslip, Betslip.class));

    Mockito.verify(notificationsFactory, Mockito.never()).notify(getDevice(), getPayload());

    Mockito.verify(template, Mockito.never()).delete(MOCK_KEY);
  }

  private Device getDevice() {
    return new Device(MOCK_TOKEN, Platform.ANDROID, null);
  }

  private Payload getPayload() {
    return Payload.builder()
        .message(NOTIFICATION_TITLE)
        .status(WELL_FORMATTED_MESSAGE)
        .deepLink(DEEP_LINK)
        .type("winalert")
        .build();
  }
}
