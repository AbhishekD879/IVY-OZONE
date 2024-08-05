package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.*;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxyegn.test.utils.Utils;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.MessageType;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.Position;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.ContentConverter;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.handler.NotificationMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.handler.football.KickOffMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class MessageHandlerTest extends BDDMockito {

  private Gson gson = new GsonBuilder().create();
  private static final String DEEP_LINK_MOCK =
      "horse-racing/-horse-racing-live-/la-teste-de-buch/-12-00-la-teste-de-buch-/";
  private static final String OWNER_ID_MOCK = "ownerId";
  private static final String TOKEN_MOCK = "token";
  private static final long EVENT_ID_MOCK = 12442253;
  private static final long OUTCOME_ID_MOCK = 949641126;
  private static final int ONCE = 1;
  private static final int NEVER = 0;

  private static final String PAYLOAD_TITLE = "20:58 Grand National Event";
  private static final String PAYLOAD_KICK_OFF = "Kick Off!";

  private static final String GOING_DOWN_STATUS =
      "The 20:58 at Grand National Event is starting in 2 minutes. See the latest odds here.";
  private static final String RACE_OFF_STATUS = "The 20:58 at Grand National Event has started.";
  private static final String NON_RUNNER_STATUS =
      "Puddymore in the 20:58 Grand National Event is a non-runner. See the latest odds here.";
  private static final String RESULTS_STATUS =
      "20:58  Grand National Event Result: 1st Phantom Wind, 2nd Oxygen Breath, 3rd Funny Phoenix, 4th Cool T";
  private static final String STREAM_STARTING_STATUS =
      "The 20:58 Grand National Event is now available to stream. Click to watch the race now.";
  private static final String FOOTBALL_STATUS = "Uzhhorod v Mukacheve";

  @Mock private Events events;

  @Mock private Subscriptions subscriptions;

  @Mock private EventService eventService;

  @Mock private NotificationsFactory notificationsFactory;

  private String goingDownUpdate;
  private String nonRunnerUpdate;
  private String raceOffUpdate;
  private String resultsUpdate;
  private String streamUpdate;
  private String kickOffUpdate;

  private NotificationMessageHandler goingDownMessageHandler;
  private NotificationMessageHandler nonRunnerMessageHandler;
  private NotificationMessageHandler raceOffMessageHandler;
  private NotificationMessageHandler resultsMessageHandler;
  private NotificationMessageHandler streamMessageHandler;
  private NotificationMessageHandler kickOffMessageHandler;

  private List<SubscriptionDTO> subscriptionDTOS;
  private List<Position> positions;

  @Before
  public void setUp() throws IOException {
    initSubscriptions();
    initPositions();

    goingDownUpdate =
        Utils.fromResource("sportsbook/going_down_update.json", this.getClass().getClassLoader());
    nonRunnerUpdate =
        Utils.fromResource("sportsbook/non_runner_update.json", this.getClass().getClassLoader());
    raceOffUpdate =
        Utils.fromResource("sportsbook/race_off_update.json", this.getClass().getClassLoader());
    resultsUpdate =
        Utils.fromResource("sportsbook/results_update.json", this.getClass().getClassLoader());
    streamUpdate =
        Utils.fromResource(
            "sportsbook/stream_starting_update.json", this.getClass().getClassLoader());
    kickOffUpdate = Utils.fromResource("messages/sICENT.json", this.getClass().getClassLoader());

    ContentConverter contentConverter = new ContentConverter(gson);

    goingDownMessageHandler =
        new GoingDownMessageHandler(
            gson, events, subscriptions, eventService, notificationsFactory);
    nonRunnerMessageHandler =
        new NonRunnerMessageHandler(
            gson, events, subscriptions, eventService, notificationsFactory, contentConverter);
    raceOffMessageHandler =
        new RaceOffMessageHandler(gson, events, subscriptions, eventService, notificationsFactory);
    resultsMessageHandler =
        new ResultsMessageHandler(
            gson, 4, events, subscriptions, eventService, notificationsFactory);
    streamMessageHandler =
        new StreamStartingMessageHandler(
            gson, events, subscriptions, eventService, notificationsFactory);

    kickOffMessageHandler =
        new KickOffMessageHandler(gson, events, subscriptions, eventService, notificationsFactory);

    Event event =
        Event.builder()
            .eventId(EVENT_ID_MOCK)
            .name("|Grand National Event|")
            .startTime("2019-06-29T19:58:00Z")
            .categoryId("21")
            .sportUri(DEEP_LINK_MOCK)
            .homeTeamName("Uzhhorod")
            .awayTeamName("Mukacheve")
            .build();

    Mockito.when(eventService.process(EVENT_ID_MOCK)).thenReturn(event);

    Mockito.when(eventService.getEventForOutcome(String.valueOf(OUTCOME_ID_MOCK)))
        .thenReturn(event);

    Mockito.when(subscriptions.findByEventId(EVENT_ID_MOCK)).thenReturn(subscriptionDTOS);

    Mockito.when(eventService.getResultsForEvent(EVENT_ID_MOCK)).thenReturn(positions);
  }

  private void initSubscriptions() {
    subscriptionDTOS = new ArrayList<>();

    subscriptionDTOS.add(forType(GOING_DOWN));
    subscriptionDTOS.add(forType(RACE_OFF));
    subscriptionDTOS.add(forType(NON_RUNNER));
    subscriptionDTOS.add(forType(RESULTS));
    subscriptionDTOS.add(forType(STREAM_STARTING));
    subscriptionDTOS.add(
        SubscriptionDTO.builder()
            .eventId(EVENT_ID_MOCK)
            .platform(Platform.ANDROID)
            .type("kick_off")
            .ownerId(OWNER_ID_MOCK)
            .token(TOKEN_MOCK)
            .build());
  }

  private SubscriptionDTO forType(MessageType type) {
    return SubscriptionDTO.builder()
        .eventId(EVENT_ID_MOCK)
        .platform(Platform.ANDROID)
        .type(type.getType())
        .ownerId(OWNER_ID_MOCK)
        .token(TOKEN_MOCK)
        .build();
  }

  private void initPositions() {
    positions = new ArrayList<>();
    positions.add(
        Position.builder().name("|Phantom Wind|").id("0").position(1).runnerNumber(1).build());
    positions.add(
        Position.builder().name("|Oxygen Breath|").id("1").position(2).runnerNumber(2).build());
    positions.add(
        Position.builder().name("|Funny Phoenix|").id("2").position(3).runnerNumber(3).build());
    positions.add(Position.builder().name("|Cool T|").id("3").position(4).runnerNumber(4).build());
    positions.add(
        Position.builder().name("|Britney Spears|").id("4").position(5).runnerNumber(5).build());
  }

  private Payload getPayloadFor(String status, MessageType type) {
    return Payload.builder()
        .eventId(EVENT_ID_MOCK)
        .message(PAYLOAD_TITLE)
        .status(status)
        .type(type.getType())
        .deepLink(DEEP_LINK_MOCK)
        .devices(Collections.singletonList(getDevice()))
        .build();
  }

  private Device getDevice() {
    return new Device(TOKEN_MOCK, Platform.ANDROID, null);
  }

  @Test
  public void goingDownPayloadTest() {
    goingDownMessageHandler.handle(goingDownUpdate);

    Mockito.verify(notificationsFactory, Mockito.times(ONCE))
        .notify(getDevice(), getPayloadFor(GOING_DOWN_STATUS, GOING_DOWN));

    Mockito.verify(subscriptions, Mockito.times(ONCE)).delete(subscriptionDTOS.get(0));
  }

  @Test
  public void raceOffPayloadTest() {
    raceOffMessageHandler.handle(raceOffUpdate);

    Mockito.verify(notificationsFactory, Mockito.times(ONCE))
        .notify(getDevice(), getPayloadFor(RACE_OFF_STATUS, RACE_OFF));

    Mockito.verify(subscriptions, Mockito.times(ONCE)).delete(subscriptionDTOS.get(1));
  }

  @Test
  public void nonRunnerPayloadTest() {
    nonRunnerMessageHandler.handle(nonRunnerUpdate);

    Mockito.verify(notificationsFactory, Mockito.times(ONCE))
        .notify(getDevice(), getPayloadFor(NON_RUNNER_STATUS, NON_RUNNER));

    Mockito.verify(subscriptions, Mockito.times(NEVER)).delete(subscriptionDTOS.get(2));
  }

  @Test
  public void nonRunnerDuplicatePayloadTest() {
    int selNUpdates = 10;
    int waitMs = 1000;
    Executor executor = Executors.newFixedThreadPool(selNUpdates);
    CountDownLatch countDownLatch = new CountDownLatch(selNUpdates);
    for (int i = 0; i < selNUpdates; i++) {
      executor.execute(
          () -> {
            countDownLatch.countDown();
            try {
              countDownLatch.await();
            } catch (InterruptedException e) {
              e.printStackTrace();
            }
            nonRunnerMessageHandler.handle(nonRunnerUpdate);
          });
    }

    // wait to make sure all nonRunnerMessageHandler.handle run
    long beforeWhileMillis = System.currentTimeMillis();
    while (System.currentTimeMillis() - beforeWhileMillis < waitMs) {}

    then(notificationsFactory)
        .should(times(ONCE))
        .notify(getDevice(), getPayloadFor(NON_RUNNER_STATUS, NON_RUNNER));
    then(subscriptions).should(times(NEVER)).delete(subscriptionDTOS.get(2));
  }

  @Test
  public void resultsPayloadTest() {
    resultsMessageHandler.handle(resultsUpdate);

    Mockito.verify(notificationsFactory, Mockito.times(ONCE))
        .notify(getDevice(), getPayloadFor(RESULTS_STATUS, RESULTS));

    Mockito.verify(subscriptions, Mockito.times(ONCE)).delete(subscriptionDTOS.get(3));
  }

  @Test
  public void streamPayloadTest() {
    streamMessageHandler.handle(streamUpdate);

    Mockito.verify(notificationsFactory, Mockito.times(ONCE))
        .notify(getDevice(), getPayloadFor(STREAM_STARTING_STATUS, STREAM_STARTING));

    Mockito.verify(subscriptions, Mockito.times(ONCE)).delete(subscriptionDTOS.get(4));
  }

  @Test
  public void kickOffTest() {
    kickOffMessageHandler.handle(kickOffUpdate);

    Mockito.verify(notificationsFactory, Mockito.times(ONCE))
        .notify(
            getDevice(),
            Payload.builder()
                .eventId(EVENT_ID_MOCK)
                .message(PAYLOAD_KICK_OFF)
                .status(FOOTBALL_STATUS)
                .type("kick_off")
                .deepLink(DEEP_LINK_MOCK)
                .devices(Collections.singletonList(getDevice()))
                .build());
  }
}
