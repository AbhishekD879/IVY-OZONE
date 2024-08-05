package com.ladbrokescoral.oxygen.notification.services.handler.football;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.handler.AbstractNotificationMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public abstract class AbstractFootballNotificationMessageHandler
    extends AbstractNotificationMessageHandler {

  public AbstractFootballNotificationMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  public abstract Payload process(String message);

  protected String statusForEvent(Event event) {
    if (!event.isLive() && (event.getAwayTeamScore() + event.getHomeTeamScore()) == 0) {
      return String.format("%s v %s", event.getHomeTeamName(), event.getAwayTeamName());
    } else {
      return String.format(
          "%s %d - %d %s",
          event.getHomeTeamName(),
          event.getHomeTeamScore(),
          event.getAwayTeamScore(),
          event.getAwayTeamName());
    }
  }

  Payload getPayloadFor(String message, String scorer, Event event, String type) {
    List<Device> devicesForType = getDevices(type, event.getEventId());

    Payload payload =
        Payload.builder()
            .message(message + scorer)
            .eventId(event.getEventId())
            .type(type)
            .status(statusForEvent(event))
            .devices(devicesForType)
            .deepLink(event.getSportUri())
            .build();

    logger.debug("Sending notification: " + payload.toString());
    return payload;
  }
}
