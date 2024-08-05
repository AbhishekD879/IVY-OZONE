package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.GOING_DOWN;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Implementation that handles "going_down" events */
@Component
public class GoingDownMessageHandler extends BaseHorsesMessageHandler {

  private static final String GOING_DOWN_MESSAGE =
      "The %s at %s is starting in 2 minutes. See the latest odds here.";

  @Autowired
  public GoingDownMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  @Override
  protected String getType() {
    return GOING_DOWN.getType();
  }

  @Override
  protected String getMessage(Event event) {
    return String.format(
        GOING_DOWN_MESSAGE, getMeetingTime(event.getStartTime()), formatEventName(event));
  }
}
