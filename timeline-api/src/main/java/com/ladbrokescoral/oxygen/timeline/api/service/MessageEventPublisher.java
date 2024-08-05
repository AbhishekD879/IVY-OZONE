package com.ladbrokescoral.oxygen.timeline.api.service;

import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import io.vavr.control.Try;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationEventPublisher;

@Slf4j
public abstract class MessageEventPublisher<M extends Message> {

  @Autowired private ApplicationEventPublisher eventPublisher;

  @Autowired private SelectionService selectionService;

  public final void publish(M message) {
    eventPublisher.publishEvent(message);
  }

  protected void runSelectionSpecificLogic(PostMessage message) {
    if (isPostWithSelection(message)) {
      Try.of(() -> selectionService.subscribeOnUpdates(message.getTemplate().getSelectionId()))
          .onSuccess(message::setSelectionEvent)
          .orElseRun(ex -> log.error("Site Server call failed", ex));
    }
  }

  private boolean isPostWithSelection(PostMessage message) {
    return message != null
        && message.getTemplate() != null
        && StringUtils.isNotEmpty(message.getTemplate().getSelectionId());
  }
}
