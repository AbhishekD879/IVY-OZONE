package com.ladbrokescoral.oxygen.notification.services;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;

import com.egalacoral.spark.siteserver.model.Event;
import com.google.gson.Gson;
import com.ladbrokescoral.oxyegn.test.utils.EventServiceTest;
import com.ladbrokescoral.oxygen.notification.services.handler.football.ScoresMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Optional;
import org.apache.commons.io.IOUtils;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;

public class ScoresMessageHandlerTest {

  private ScoresMessageHandler scoresInNameHandler;

  @Mock private Events events;
  @Mock private Subscriptions subscriptions;
  private EventService eventService;
  @Mock private NotificationsFactory notificationsFactory;
  @Mock private SiteServerApiService siteServerService;

  @Before
  public void setUp() throws Exception {
    notificationsFactory = Mockito.mock(NotificationsFactory.class);
    events = Mockito.mock(Events.class);
    siteServerService = Mockito.mock(SiteServerApiService.class);
    eventService = new EventService(siteServerService, events);
    subscriptions = Mockito.mock(Subscriptions.class);
    scoresInNameHandler =
        new ScoresMessageHandler(
            new Gson(), events, subscriptions, eventService, notificationsFactory);
    Mockito.when(events.findById(Mockito.anyString())).thenReturn(Optional.empty());
    Mockito.when(subscriptions.findByEventId(Mockito.anyLong()))
        .thenReturn(Collections.emptyList());

    String expected = getResourceAsString("events/test1lads.json");

    Mockito.when(siteServerService.getEvent(Mockito.anyString()))
        .thenReturn(Optional.of(new Gson().fromJson(expected, Event.class)));
    String commentory = getResourceAsString("events/commentory1lads.json");

    Mockito.when(siteServerService.getCommentaryForEvent(Mockito.anyString()))
        .thenReturn(Optional.of(new Gson().fromJson(commentory, Event.class)));
  }

  @Test
  public void noExceptionIfCouldNotParseEventName() {

    scoresInNameHandler.onApplicationEvent(
        new ScoreChangedEvent(
            new Object(),
            ScoresDto.builder()
                .eventId(1L)
                .homeScore(1)
                .awayScore(3)
                .homePenalties(0)
                .awayPenalties(0)
                .build()));

    Mockito.verify(notificationsFactory, never()).notify(any(), any());
  }

  private String getResourceAsString(String name) throws IOException {
    return IOUtils.toString(
        EventServiceTest.class.getClassLoader().getResourceAsStream(name), StandardCharsets.UTF_8);
  }
}
