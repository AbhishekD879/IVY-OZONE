package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.EventStatus;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.ObEvent;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
@Slf4j
public class EventMessageApplier extends ChannelMessageApplier {

  private final PostRepository postRepository;

  public EventMessageApplier(ObjectMapper mapper, PostRepository postRepository) {
    super(mapper);
    this.postRepository = postRepository;
  }

  @Override
  public List<PostMessage> applyUpdate(MessageEnvelope messageEnvelope) {
    return parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), EventStatus.class)
        .map(
            (EventStatus eventStatus) -> {
              String eventId = getUpdateMessageId(messageEnvelope);
              return findAndUpdatePosts(eventStatus, eventId);
            })
        .orElse(Collections.emptyList());
  }

  @NotNull
  private List<PostMessage> findAndUpdatePosts(EventStatus eventStatus, String eventId) {
    List<PostMessage> postMessages = new ArrayList<>();
    Iterable<PostMessage> postMessageIterator = postRepository.findAll();
    postMessageIterator.forEach(postMessages::add);
    List<PostMessage> filteredPostMessages = new ArrayList<>();
    postMessages.stream()
        .filter(this::isPostWithEvent)
        .filter(postMessage -> eventId.equals(postMessage.getSelectionEvent().getObEvent().getId()))
        .forEach(postMessage -> eventUpdate(postMessage, eventStatus, filteredPostMessages));
    return filteredPostMessages;
  }

  private void eventUpdate(
      PostMessage postMessage, EventStatus eventStatus, List<PostMessage> filteredPostMessages) {
    ObEvent event = postMessage.getSelectionEvent().getObEvent();
    event.applyEventUpdate(eventStatus);
    postRepository.save(postMessage);
    filteredPostMessages.add(postMessage);
  }

  @Override
  protected String type() {
    return "sEVENT";
  }

  private boolean isPostWithEvent(PostMessage postMessage) {
    return StringUtils.hasText(postMessage.getTemplate().getSelectionId())
        && postMessage.getSelectionEvent() != null
        && postMessage.getSelectionEvent().getObEvent() != null;
  }
}
