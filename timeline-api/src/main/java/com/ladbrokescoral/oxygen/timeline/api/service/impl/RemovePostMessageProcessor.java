package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.RemovePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageEventPublisher;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class RemovePostMessageProcessor extends MessageEventPublisher<RemovePostMessage>
    implements MessageProcessor<RemovePostMessage> {
  private final PostRepository postRepository;

  @Override
  public void process(RemovePostMessage message) {
    postRepository.deleteById(message.getAffectedMessageId());
    publish(message);
  }
}
