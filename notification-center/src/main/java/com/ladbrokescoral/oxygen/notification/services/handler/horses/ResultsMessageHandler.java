package com.ladbrokescoral.oxygen.notification.services.handler.horses;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.RESULTS;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.notification.entities.Position;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.EventService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.services.repositories.Events;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/** Implementation that handles "results" events */
@Slf4j
@Component
public class ResultsMessageHandler extends BaseHorsesMessageHandler {

  private static final String RESULTS_MESSAGE = "%s  %s Result: %s";
  private static final Map<Integer, String> ordinals;
  private long maxRunnersResults;

  static {
    ordinals = new HashMap<>();
    ordinals.put(1, "1st ");
    ordinals.put(2, "2nd ");
    ordinals.put(3, "3rd ");
    ordinals.put(4, "4th ");
  }

  @Autowired
  public ResultsMessageHandler(
      Gson gson,
      @Value("${application.runner-results.max}") long maxRunnersResults,
      Events events,
      Subscriptions subscriptions,
      EventService eventService,
      NotificationsFactory notificationsFactory) {
    super(gson, events, subscriptions, eventService, notificationsFactory);
    this.maxRunnersResults = maxRunnersResults;
  }

  @Override
  protected String getType() {
    return RESULTS.getType();
  }

  @Override
  protected String getMessage(Event event) {
    return Optional.ofNullable(getResult(event))
        .map(
            results ->
                String.format(
                    RESULTS_MESSAGE,
                    getMeetingTime(event.getStartTime()),
                    formatEventName(event),
                    results))
        .orElse(null);
  }

  /**
   * Obtains results for event from siteserver, sorts positions, filters them to certain limit,
   * formats and converts it to single string.
   */
  private String getResult(Event event) {
    logger.info(
        "[RACING FLOW][RESULTS][{}]: Obtaining results for event: {}", event.getEventId(), event);

    List<Position> positions = eventService.getResultsForEvent(event.getEventId());

    logger.info(
        "[RACING FLOW][RESULTS][{}]: Obtained results: {} /n For event: {}",
        positions.toString(),
        event.getId(),
        event);

    List<String> results =
        positions.stream()
            .filter(position -> position.getPosition() != 0)
            .sorted(Comparator.comparingInt(Position::getPosition))
            .limit(maxRunnersResults)
            .map(
                position ->
                    ordinals.get(position.getPosition()) + position.getName().replace("|", ""))
            .collect(Collectors.toList());
    if (results.isEmpty()) {
      logger.warn(
          "[RACING FLOW][RESULTS][{}]: Did not obtain any results for event: {}",
          event.getEventId(),
          event);
      return null;
    } else {
      String resultString = getSingleResultString(results);
      logger.info(
          "[RACING FLOW][RESULTS][{}]: Created results string: {} /n For event: {}",
          event.getEventId(),
          resultString,
          event);
      return resultString;
    }
  }

  private String getSingleResultString(List<String> results) {
    String result = results.stream().map(s -> s + ", ").collect(Collectors.joining());
    return result.substring(0, result.length() - 2);
  }
}
