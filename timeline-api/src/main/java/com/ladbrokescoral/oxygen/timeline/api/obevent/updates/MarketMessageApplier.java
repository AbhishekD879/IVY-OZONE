package com.ladbrokescoral.oxygen.timeline.api.obevent.updates;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.MarketStatus;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.ObMarket;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@Slf4j
@Component
public class MarketMessageApplier extends ChannelMessageApplier {

  private final PostRepository postRepository;

  public MarketMessageApplier(ObjectMapper mapper, PostRepository postRepository) {
    super(mapper);
    this.postRepository = postRepository;
  }

  @Override
  public List<PostMessage> applyUpdate(MessageEnvelope messageEnvelope) {
    return parseLiveUpdateData(messageEnvelope.getMessage().getJsonData(), MarketStatus.class)
        .map(
            (MarketStatus marketStatus) -> {
              String marketId = getUpdateMessageId(messageEnvelope);
              return findAndUpdatePosts(marketStatus, marketId);
            })
        .orElse(Collections.emptyList());
  }

  @NotNull
  private List<PostMessage> findAndUpdatePosts(MarketStatus marketStatus, String marketId) {
    List<PostMessage> postMessages = new ArrayList<>();
    Iterable<PostMessage> postMessageIterator = postRepository.findAll();
    postMessageIterator.forEach(postMessages::add);
    postMessages =
        postMessages.stream()
            .filter(this::isPostWithMarket)
            .filter(
                postMessage -> postMessage.getSelectionEvent().queryMarketIds().contains(marketId))
            .collect(Collectors.toCollection(ArrayList::new));

    return postMessages.stream()
        .peek(
            postMessage ->
                postMessage
                    .getSelectionEvent()
                    .getMarketById(marketId)
                    .ifPresent(
                        (ObMarket obMarket) -> marketUpdate(obMarket, marketStatus, postMessage)))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private void marketUpdate(ObMarket obMarket, MarketStatus marketStatus, PostMessage postMessage) {
    obMarket.applyMarketUpdate(marketStatus);
    postRepository.save(postMessage);
  }

  @Override
  protected String type() {
    return "sEVMKT";
  }

  private boolean isPostWithMarket(PostMessage postMessage) {
    return isPostWithEvent(postMessage)
        && !CollectionUtils.isEmpty(postMessage.getSelectionEvent().getObEvent().getMarkets());
  }

  private boolean isPostWithEvent(PostMessage postMessage) {
    return StringUtils.hasText(postMessage.getTemplate().getSelectionId())
        && postMessage.getSelectionEvent() != null
        && postMessage.getSelectionEvent().getObEvent() != null;
  }
}
