package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Event;
import com.ladbrokescoral.cashout.service.SelectionData;
import com.newrelic.api.agent.NewRelic;
import java.math.BigInteger;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class EventUpdateProcessor extends AbstractUpdateProcessor<Event>
    implements UpdateProcessor<Event> {

  @Value("${vod.eventUpdate.flags}")
  private String eventUpdateFlags;

  private final EventUpdatePublisher eventUpdatePublisher;
  private static final String KAFKA_MESSAGES_EVENT = "/Kafka/Messages/Event";
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public EventUpdateProcessor(
      SelectionDataAwareUpdateProcessor<Event> processor,
      EventUpdatePublisher eventUpdatePublisher) {
    super(processor);
    this.eventUpdatePublisher = eventUpdatePublisher;
  }

  /*-
   * Call BPP betDetail in case update events related to bet
   *
   * @param context     - User related data
   * @param eventUpdate - kafka Saf event update
   */
  @Override
  public void process(UserRequestContextAccHistory context, Event eventUpdate) {
    NewRelic.incrementCounter(KAFKA_MESSAGES_EVENT);

    ASYNC_LOGGER.debug(
        "EventUpdateProcessor eventId : {}, isEventFinished : {}",
        eventUpdate.getEventKey(),
        eventUpdate.isEventFinished());
    BigInteger eventId = eventUpdate.getEventKey();
    Set<SelectionData> selectionsDataSet =
        context.getIndexedData().getSelectionDataByEventId(eventId);
    if (Objects.nonNull(eventUpdate.getIsEventStarted()) && Objects.nonNull(selectionsDataSet)) {
      selectionsDataSet.forEach(eventUpdate::applyEventStartedChange);
    }

    executeEventUpdateRequest(context.getToken(), eventUpdate, selectionsDataSet, eventId);

    if (!isUpdateImportant(eventUpdate) || eventId == null) {
      return;
    }

    selectionDataAwareUpdateProcessor.processUpdateWithSelectionDataInContext(
        context, eventUpdate, selectionsDataSet);
  }

  @SuppressWarnings("java:S3655")
  private void executeEventUpdateRequest(
      String token, Event eventUpdate, Set<SelectionData> selectionsDataSet, BigInteger eventId) {
    if (eventUpdate.isEventFinished() && !CollectionUtils.isEmpty(selectionsDataSet)) {
      SelectionData selectionData = selectionsDataSet.stream().findFirst().get();
      String flags = selectionData.getParts().get(0).getOutcome().get(0).getEvent().getFlags();
      List<String> eventFlags =
          Stream.of(flags.split(",")).map(String::trim).collect(Collectors.toList());
      List<String> updateFlags =
          Stream.of(eventUpdateFlags.split(",")).map(String::trim).collect(Collectors.toList());
      if (eventFlags.stream().anyMatch(updateFlags::contains)) {
        ASYNC_LOGGER.debug("eventUpdate published for eventId : {}", eventId);
        eventUpdatePublisher.eventUpdateRequest(token, eventId);
      }
    }
  }

  private boolean isUpdateImportant(Event event) {
    return statusesChanged(event);
  }

  private boolean statusesChanged(Event event) {
    return Objects.nonNull(event.getEventStatus());
  }
}
