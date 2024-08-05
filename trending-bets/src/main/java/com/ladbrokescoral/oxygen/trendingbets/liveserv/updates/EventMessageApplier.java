package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.EventStatus;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.service.PopularBetUpdateService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class EventMessageApplier extends ChannelMessageApplier {

  public EventMessageApplier(
      ObjectMapper mapper,
      PopularBetUpdateService eventService,
      @Lazy LiveServService liveServService) {
    super(mapper, eventService, liveServService);
  }

  @Override
  public void applyUpdate(MessageEnvelope messageEnvelope) {
    Optional<EventStatus> eventStatus =
        parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), EventStatus.class);
    log.info("event status {}", eventStatus);

    if (eventStatus.isPresent() && isValidChannel(messageEnvelope.getChannel())) {
      TrendingBetsContext.clearEventContextForLiveEvents(
              eventService.updateEvent(eventStatus.get(), messageEnvelope.getChannel()))
          .stream()
          .flatMap(TrendingEvent::getStreamChannels)
          .forEach(this::unsubscribe);
    }
  }

  @Override
  protected String type() {
    return "sEVENT";
  }
}
