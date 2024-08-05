package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.RACE_OFF;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Implementation that handles "race_off" events */
@Component
public class RaceOffMessageHandler extends BaseHorsesMessageHandler {

  private static final String RACE_OFF_MESSAGE = "The %s at %s has started.";

  @Autowired
  public RaceOffMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  @Override
  protected String getType() {
    return RACE_OFF.getType();
  }

  @Override
  protected String getMessage(Event event) {
    return String.format(
        RACE_OFF_MESSAGE, getMeetingTime(event.getStartTime()), formatEventName(event));
  }
}
