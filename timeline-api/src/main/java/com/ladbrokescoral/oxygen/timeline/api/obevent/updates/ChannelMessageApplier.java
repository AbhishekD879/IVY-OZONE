package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.AbstractStatus;
import com.newrelic.api.agent.NewRelic;
import java.util.List;
import java.util.Optional;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public abstract class ChannelMessageApplier {

  private static final int BEGIN_INDEX = 6;

  @Getter(AccessLevel.PROTECTED)
  private final ObjectMapper mapper;

  protected ChannelMessageApplier(ObjectMapper mapper) {
    this.mapper = mapper;
  }

  public abstract List<PostMessage> applyUpdate(MessageEnvelope messageEnvelope);

  protected abstract String type();

  protected <T extends AbstractStatus> Optional<T> parseLiveUpdateData(
      String liveUpdateData, Class<T> type) {
    try {
      return Optional.of(getMapper().readValue(liveUpdateData, type));
    } catch (JsonProcessingException e) {
      log.error("Failed to parse live update", e);
      NewRelic.noticeError("Failed to parse live update. " + e.getMessage());
    }
    return Optional.empty();
  }

  protected String getUpdateMessageId(MessageEnvelope messageEnvelope) {
    return StringUtils.normalizeNumber(messageEnvelope.getChannel().substring(BEGIN_INDEX));
  }
}
