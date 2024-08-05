package com.ladbrokescoral.oxygen.notification.services.handler;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

/**
 * A base handler for all notification types, except of Win-Alert type, since the handling logic is
 * different for it.
 */
@Slf4j
public abstract class AbstractNotificationMessageHandler
    implements NotificationMessageHandler<String> {

  protected Gson gson;
  protected Events events;
  protected EventService eventService;
  protected Subscriptions subscriptions;
  private NotificationsFactory notificationsFactory;

  public AbstractNotificationMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    this.gson = gson;
    this.events = events;
    this.subscriptions = subscriptions;
    this.eventService = eventService;
    this.notificationsFactory = notificationsFactory;
  }

  @Override
  public void handle(String message) {
    Payload payload = process(message);
    publishPayload(payload);
  }

  /**
   * In case if there are subscribers for this update, will send the push notification via
   * NotificationsFactory.java
   *
   * @param payload to send notification with
   */
  protected void publishPayload(Payload payload) {
    if (!payload.getDevices().isEmpty()) {

      logger.info(
          "[RACING FLOW][{}][{}]: Successfully created payload with subscribers: {}",
          payload.getType().toUpperCase(),
          payload.getEventId(),
          payload);

      payload
          .getDevices()
          .parallelStream()
          .forEach(device -> notificationsFactory.notify(device, payload));
    }
  }

  /**
   * Implement specific way to handle update for specific type
   *
   * @param message is an update itself
   * @return a contents of a push message with metadata (Platform, token, etc)
   */
  public abstract Payload process(String message);

  /**
   * Searches cache for the event. If it is not in cache, will try to get it from siteserver.
   *
   * @param eventId of the event that is to be searched
   * @return the event from either cache or siteserver
   */
  protected Event getEventById(Long eventId) {
    String idToFind = RedisKey.forEvent(eventId);
    try {
      return events
          .findById(idToFind)
          .orElseGet(
              () -> {
                logger.warn("Can't find event {} in cache. Re-consuming it.", eventId);
                return eventService.process(eventId);
              });
    } catch (Exception exception) {
      events.deleteAll();
      return eventService.process(eventId);
    }
  }

  /** Provides a list of subscribers, subscribed on given event and type. */
  protected List<SubscriptionDTO> getSubscribers(String type, long eventId) {
    logger.info(
        "[RACING FLOW][{}][{}]: Obtaining subscribers for update.", type.toUpperCase(), eventId);

    List<SubscriptionDTO> subscribers =
        subscriptions.findByEventId(eventId).stream()
            .filter(Objects::nonNull)
            .filter(s -> Objects.nonNull(s.getType()) && s.getType().equals(type))
            .collect(Collectors.toList());

    logger.info(
        "[RACING FLOW][{}][{}]: Obtained subscribers for update: {} ",
        type.toUpperCase(),
        eventId,
        subscribers.toString());

    return subscribers;
  }

  /**
   * Obtains a list of subscribers and converts it to the list of devices (platform,
   * token,AppVersionInt)
   */
  protected List<Device> getDevices(String type, long eventId) {

    List<Device> devices =
        getSubscribers(type, eventId).stream()
            .map(s -> new Device(s.getToken(), s.getPlatform(), s.getAppVersionInt()))
            .distinct()
            .collect(Collectors.toList());

    logger.info(
        "[RACING FLOW][{}][{}]: Obtained devices for update: {}",
        type.toUpperCase(),
        eventId,
        devices.toString());

    return devices;
  }
}
