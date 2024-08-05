package com.ladbrokescoral.oxygen.notification.services.handler.football;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.IncidentMessage;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class KickOffMessageHandler extends AbstractFootballNotificationMessageHandler {

  private static final String TYPE = "kick_off";
  private static final String KICKOFF_MESSAGE = "Kick Off!";
  private static final String SCORER = "";

  @Autowired
  public KickOffMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  @Override
  protected String statusForEvent(Event event) {
    return event.getHomeTeamName() + " v " + event.getAwayTeamName();
  }

  @Override
  public Payload process(String json) {
    try {
      final IncidentMessage message = gson.fromJson(json, IncidentMessage.class);
      long eventId = message.getEventId();
      final Event event = getEventById(eventId);

      if (message.getRelativeTime() == 0 && !event.isLive()) {
        events.save(event.setLive(true));
        return getPayloadFor(KICKOFF_MESSAGE, SCORER, event, TYPE);
      }
      return Payload.builder().build();
    } catch (Exception e) {
      logger.error("Error during processing cards", e);
      return Payload.builder().build();
    }
  }
}
