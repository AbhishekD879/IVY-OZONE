package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.STREAM_STARTING;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import org.springframework.stereotype.Component;

/** Implementation that handles "stream_starting" events */
@Component
public class StreamStartingMessageHandler extends BaseHorsesMessageHandler {

  private static final String STREAM_STARTED_MESSAGE =
      "The %s %s is now available to stream. Click to watch the race now.";

  public StreamStartingMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  @Override
  protected String getType() {
    return STREAM_STARTING.getType();
  }

  @Override
  protected String getMessage(Event event) {
    return String.format(
        STREAM_STARTED_MESSAGE, getMeetingTime(event.getStartTime()), formatEventName(event));
  }
}
