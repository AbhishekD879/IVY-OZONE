package com.gvc.oxygen.betreceipts.liveserv.updates;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.liveserv.domain.AbstractStatus;
import java.util.Optional;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public abstract class ChannelMessageApplier {

  public static final int CHANNEL_LIMIT = 6;

  @Getter(AccessLevel.PROTECTED)
  private final ObjectMapper mapper;

  protected ChannelMessageApplier(ObjectMapper mapper) {
    this.mapper = mapper;
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
}
