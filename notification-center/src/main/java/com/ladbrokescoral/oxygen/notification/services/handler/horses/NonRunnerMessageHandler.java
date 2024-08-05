package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.NON_RUNNER;
import static com.ladbrokescoral.oxygen.notification.services.handler.AbstractSportsbookUpdateMapper.NON_RUNNER_NAME;
import static com.ladbrokescoral.oxygen.notification.utils.RepositoryStream.parallelStream;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Selection;
import com.ladbrokescoral.oxygen.notification.services.ContentConverter;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Implementation that handles "non_runner" events */
@Slf4j
@Component
public class NonRunnerMessageHandler extends BaseHorsesMessageHandler {

  private static final String NON_RUNNER_MESSAGE =
      "%s in the %s %s is a non-runner. See the latest odds here.";

  private ContentConverter contentConverter;

  @Autowired
  public NonRunnerMessageHandler(
      Gson gson,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory,
      ContentConverter contentConverter) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
    this.contentConverter = contentConverter;
  }

  @Override
  public Payload process(String message) {
    Event event = getEvent(message);
    Selection selection = getSelection(message);
    if (event != null && selection != null) {

      synchronized (event.getEventId().toString().intern()) {
        logger.info(
            "[RACING FLOW][NON RUNNER][{}]: processing update: message: {}  Event: {}. Selection: {}",
            event.getEventId(),
            message,
            event,
            selection);

        // STEP I: Find all devices for N/R filtered by sentNonRunners with SelectionName excluded
        // sentNonRunners inside subscriptions is updated in later STEP II
        List<Device> devices =
            getNonRunnerDevices(
                getType(), event.getEventId(), selection.getSelectionNameTranslated());

        if (devices.isEmpty()) {
          logger.info(
              "[RACING FLOW][{}][{}]: Canceling racing update: NO SUBSCRIBERS. Event: {}, message: {}: ",
              getType().toUpperCase(),
              event.getId(),
              event,
              message);

          return Payload.builder().build();
        }

        Payload payload = getPayloadFor(getMessage(selection, event), event, getType(), devices);

        // STEP II: update subscription with N/R EventName to prevent duplicates
        // use selection name instead of selection key since there are a lot
        // of different selection keys with the same player coming
        addNonRunnerForSubscription(payload, selection.getSelectionNameTranslated());
        return payload;
      }
    }
    return Payload.builder().build();
  }

  /** Get the list of devices which hasn't yet received non-runner for specific selection */
  private List<Device> getNonRunnerDevices(String type, long eventId, String selectionName) {
    List<SubscriptionDTO> subscriptions =
        getSubscribers(type, eventId).stream()
            .filter(
                dto ->
                    Objects.isNull(dto.getSentNonRunners())
                        || !dto.getSentNonRunners().contains(selectionName))
            .collect(Collectors.toList());

    logger.info(
        "[RACING FLOW][NON RUNNER][{}]: Filtered subscribers with no sent non runners: {}. Update type: {}",
        eventId,
        subscriptions.toString(),
        type);

    List<Device> devices =
        subscriptions.stream()
            .map(s -> new Device(s.getToken(), s.getPlatform(), s.getAppVersionInt()))
            .distinct()
            .collect(Collectors.toList());

    logger.info(
        "[RACING FLOW][NON RUNNER][{}]: Filtered devices with no sent non runners: {}. Update type: {}",
        eventId,
        devices.toString(),
        type);

    return devices;
  }

  private void addNonRunnerForSubscription(Payload payload, String selectionName) {
    Iterable<SubscriptionDTO> subsById = subscriptions.findByEventId(payload.getEventId());
    payload.getDevices().stream()
        .flatMap(
            device ->
                parallelStream(subsById)
                    .filter(dto -> dto.getPlatform().equals(device.getPlatform()))
                    .filter(dto -> dto.getToken().equals(device.getToken())))
        .filter(dto -> dto.getType().equalsIgnoreCase(NON_RUNNER.getType()))
        .forEach(dto -> addNonRunner(dto, selectionName));
  }

  private void addNonRunner(SubscriptionDTO dto, String selectionName) {
    if (dto.getSentNonRunners() == null) {
      dto.setSentNonRunners(new ArrayList<>());
    }

    dto.getSentNonRunners().add(selectionName);
    subscriptions.save(dto);

    logger.info(
        "[RACING FLOW][NON RUNNER][{}]: Added non runner for subscription: {}",
        dto.getEventId(),
        dto);
  }

  @Override
  protected String getType() {
    return NON_RUNNER.getType();
  }

  private String getMessage(Selection selection, Event event) {
    return String.format(
        NON_RUNNER_MESSAGE,
        formatRunnerName(selection),
        getMeetingTime(event.getStartTime()),
        formatEventName(event));
  }

  private String formatRunnerName(Selection selection) {
    return escapeSlash(stripNR(selection.getSelectionName()));
  }

  private String stripNR(String selectionName) {
    return selectionName.replace(NON_RUNNER_NAME, "");
  }

  @Override
  protected String getMessage(Event event) {
    // stub
    throw new IllegalStateException("Should not come here");
  }

  @Override
  protected Event getEvent(String message) {
    Selection selection = getSelection(message);
    if (selection != null) {
      return eventService.getEventForOutcome(selection.getSelectionKey());
    } else {
      logger.warn("no selection found in update for type: {}, message: {}", getType(), message);
      return null;
    }
  }

  private Selection getSelection(String message) {
    return (Selection)
        contentConverter
            .convert(message)
            .filter(entity -> entity instanceof Selection)
            .orElse(null);
  }
}
