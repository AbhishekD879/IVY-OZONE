package com.gvc.oxygen.betreceipts.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.liveserv.domain.EventStatus;
import com.gvc.oxygen.betreceipts.service.EventService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Slf4j(topic = "testpostevent")
public class EventMessageApplier extends ChannelMessageApplier {

  private final EventService eventService;

  private LiveServService liveServService;

  public EventMessageApplier(
      ObjectMapper mapper, EventService eventService, @Lazy LiveServService liveServService) {
    super(mapper);
    this.eventService = eventService;
    this.liveServService = liveServService;
  }

  @Override
  public void applyUpdate(MessageEnvelope messageEnvelope) {
    Optional<EventStatus> eventStatus =
        parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), EventStatus.class);
    log.info("event status {}", eventStatus);
    if (eventStatus.isPresent() && Boolean.TRUE.equals(eventStatus.get().getStarted())) {
      liveServService.unsubscribe(messageEnvelope.getChannel());
      eventService.deleteNextRaceMap(String.valueOf(messageEnvelope.getEventId()));
      eventService.deleteMetaEvent(String.valueOf(messageEnvelope.getEventId()));
    }
  }

  @Override
  protected String type() {
    return "sEVENT";
  }
}
