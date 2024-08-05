package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.utils.RepositoryStream.parallelStream;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookUpdate;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.handler.AbstractNotificationMessageHandler;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;
import org.springframework.beans.factory.annotation.Value;

/** A base handler for racing notification types. */
@Slf4j
public abstract class BaseHorsesMessageHandler extends AbstractNotificationMessageHandler {

  private static final String TIME_FORMAT = "HH:mm";
  private static final String TITLE_FORMAT = "%s %s";

  @Value("${timezone.default}")
  private String defaultTimeZone = "Europe/London";

  public BaseHorsesMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
  }

  /**
   * Searches storage for subscriber that is going to receive the push message. Removes matching
   * subscription from storage in order to avoid duplicating messages.
   *
   * @param payload that is going to be sent as push message
   */
  private void clearSubscriptions(Payload payload) {
    logger.info(
        "[RACING FLOW][{}][{}]: Will now clear subscriptions for payload: {}: ",
        payload.getType().toUpperCase(),
        payload.getEventId(),
        payload);

    Iterable<SubscriptionDTO> subsById = subscriptions.findByEventId(payload.getEventId());
    payload.getDevices().stream()
        .flatMap(
            device ->
                parallelStream(subsById)
                    .filter(dto -> dto.getPlatform().equals(device.getPlatform()))
                    .filter(dto -> dto.getToken().equals(device.getToken())))
        .filter(dto -> dto.getType().equals(payload.getType()))
        .forEach(this::clearDto);
  }

  private void clearDto(SubscriptionDTO dto) {
    subscriptions.delete(dto);
    logger.info(
        "[RACING FLOW][{}][{}]: Removed subscription: {}: ",
        dto.getType().toUpperCase(),
        dto.getEventId(),
        dto);
  }
  /**
   * Obtains the event linked to the update, checks, if it is a racing event. Obtains subscribers,
   * and forms the payload
   *
   * @param message is an update itself
   * @return a contents of a push message with metadata (Platform, token, etc)
   */
  @Override
  public Payload process(String message) {
    try {
      Event event = getEvent(message);
      if (isRacingEvent(event)) {
        logger.info(
            "[RACING FLOW][{}][{}]: Event for message. Event: {}, message: {}: ",
            getType().toUpperCase(),
            event.getId(),
            event,
            message);
        List<Device> devices = getDevices(getType(), event.getEventId());
        if (devices.isEmpty()) {
          // not interested in that case
          logger.info(
              "[RACING FLOW][{}][{}]: Canceling racing update: NO SUBSCRIBERS. Event: {}, message: {}: ",
              getType().toUpperCase(),
              event.getId(),
              event,
              message);
          return Payload.builder().build();
        }
        Payload payload = getPayloadFor(getMessage(event), event, getType(), devices);
        clearSubscriptions(payload);
        return payload;
      } else {
        // not interested
        logger.info(
            "[RACING FLOW][{}][{}]: Canceling racing update: Event is not racing. Event: {}, message: {}: ",
            getType().toUpperCase(),
            event.getId(),
            event,
            message);
        return Payload.builder().build();
      }
    } catch (Exception e) {
      logger.warn("Could not process update for message: " + message, e);
      return Payload.builder().build();
    }
  }

  private boolean isRacingEvent(Event event) {
    return ObjectMapper.categoryIdGreyhounds.equals(event.getCategoryId())
        || ObjectMapper.categoryIdHorses.equals(event.getCategoryId())
        || ObjectMapper.categoryIdTote.equals(event.getCategoryId());
  }

  protected Event getEvent(String message) {
    SportsBookUpdate update = gson.fromJson(message, SportsBookUpdate.class);
    Event messageEvent = update.getEvent();
    return getEventById(messageEvent.getEventId());
  }

  /** @return a type of update that is handling. */
  protected abstract String getType();

  /**
   * Forms a message for specific type and event
   *
   * @param event that is linked to update
   * @return a message that fits an update
   */
  protected abstract String getMessage(Event event);

  String getMeetingTime(String eventStartTime) {
    DateTime time = DateTime.parse(eventStartTime);
    DateTimeFormatter formatter = DateTimeFormat.forPattern(TIME_FORMAT);
    return formatter.print(time.withZone(DateTimeZone.forID(defaultTimeZone)));
  }

  /**
   * Forms a payload with data and metadata to send push notification.
   *
   * @param message the user will see
   * @param event that is linked to the update
   * @param type of update
   * @param devices that are subscribed to this update
   * @return a payload with data and metadata to send push notification.
   */
  Payload getPayloadFor(String message, Event event, String type, List<Device> devices) {
    if (message == null) {
      return Payload.builder().build();
    }
    Payload payload =
        Payload.builder()
            .message(getTitle(event))
            .eventId(event.getEventId())
            .type(type)
            .deepLink(event.getSportUri())
            .status(message)
            .devices(devices)
            .build();

    logger.info(
        "[RACING FLOW][{}][{}]: Created payload for update: {}",
        payload.getType().toUpperCase(),
        payload.getEventId(),
        payload.toString());
    return payload;
  }

  /**
   * Formats the event's name by removing vertical slash symbol '|' and removing the time from it
   *
   * @param event which name is to be extracted
   * @return extracted and formatted name as string
   */
  String formatEventName(Event event) {
    return escapeSlash(event.getName()).replace(getMeetingTime(event.getStartTime()), "").trim();
  }

  private String getTitle(Event event) {
    return String.format(
        TITLE_FORMAT, getMeetingTime(event.getStartTime()), formatEventName(event));
  }

  String escapeSlash(String eventName) {
    return eventName.replace("|", "");
  }
}
