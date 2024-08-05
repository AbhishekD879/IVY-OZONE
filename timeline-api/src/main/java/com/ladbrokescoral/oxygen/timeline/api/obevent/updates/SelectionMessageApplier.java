package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.ObOutcome;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.SelectionStatus;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
@Slf4j
public class SelectionMessageApplier extends ChannelMessageApplier {

  private final PostRepository postRepository;

  public SelectionMessageApplier(ObjectMapper mapper, PostRepository postRepository) {
    super(mapper);
    this.postRepository = postRepository;
  }

  @Override
  public List<PostMessage> applyUpdate(MessageEnvelope messageEnvelope) {
    return parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), SelectionStatus.class)
        .map(
            (SelectionStatus selectionStatus) -> {
              String selectionId = getUpdateMessageId(messageEnvelope);
              return findAndUpdatePosts(selectionStatus, selectionId);
            })
        .orElse(Collections.emptyList());
  }

  @NotNull
  private List<PostMessage> findAndUpdatePosts(
      SelectionStatus selectionStatus, String selectionId) {
    List<PostMessage> postMessages = new ArrayList<>();
    Iterable<PostMessage> postMessageIterator = postRepository.findAll();
    postMessageIterator.forEach(postMessages::add);

    postMessages =
        postMessages.stream()
            .filter(postMessage -> StringUtils.hasText(postMessage.getTemplate().getSelectionId()))
            .filter(postMessage -> selectionId.equals(postMessage.getTemplate().getSelectionId()))
            .collect(Collectors.toCollection(ArrayList::new));

    return postMessages.stream()
        .filter(postMessage -> postMessage.getSelectionEvent() != null)
        .peek(applyOutcomeUpdate(selectionStatus, selectionId))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  @NotNull
  private Consumer<PostMessage> applyOutcomeUpdate(
      SelectionStatus selectionStatus, String selectionId) {
    return postMessage ->
        postMessage
            .getSelectionEvent()
            .getOutcomeById(selectionId)
            .ifPresent(
                (ObOutcome obOutcome) -> selectionUpdate(obOutcome, selectionStatus, postMessage));
  }

  private void selectionUpdate(
      ObOutcome obOutcome, SelectionStatus selectionStatus, PostMessage postMessage) {
    obOutcome.applyOutcomeLiveUpdate(selectionStatus);
    postRepository.save(postMessage);
  }

  @Override
  protected String type() {
    return "sSELCN";
  }
}
