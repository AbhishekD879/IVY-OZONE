package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.liveserv.domain.AbstractStatus;
import com.ladbrokescoral.oxygen.trendingbets.service.PopularBetUpdateService;
import java.util.Optional;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public abstract class ChannelMessageApplier {

  protected final PopularBetUpdateService eventService;
  protected final LiveServService liveServService;

  @Getter(AccessLevel.PROTECTED)
  private final ObjectMapper mapper;

  protected ChannelMessageApplier(
      ObjectMapper mapper, PopularBetUpdateService eventService, LiveServService liveServService) {
    this.mapper = mapper;
    this.eventService = eventService;
    this.liveServService = liveServService;
  }

  public abstract void applyUpdate(MessageEnvelope messageEnvelope);

  protected abstract String type();

  protected <T extends AbstractStatus> Optional<T> parseLiveUpdateData(
      String liveUpdateData, Class<T> type) {
    try {
      return Optional.of(getMapper().readValue(liveUpdateData, type));
    } catch (JsonProcessingException e) {
      log.error("Failed to parse live update", e);
    }
    return Optional.empty();
  }

  protected boolean isValidChannel(String channel) {
    if (TrendingBetsContext.getPopularSelections().keySet().contains(channel)
        || TrendingBetsContext.getPersonalizedSelections().keySet().contains(channel)) {

      return true;
    } else {
      unsubscribe(channel);
      return false;
    }
  }

  protected void unsubscribe(String channel) {
    log.error("UNSUBSCRIBING :: {}", channel);
    TrendingBetsContext.getSubscribedChannels().remove(channel);
    liveServService.unsubscribe(channel);
  }
}
