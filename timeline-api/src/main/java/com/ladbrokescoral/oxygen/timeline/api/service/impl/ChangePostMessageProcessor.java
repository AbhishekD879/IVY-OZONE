package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageEventPublisher;
import com.ladbrokescoral.oxygen.timeline.api.service.MessageProcessor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@RequiredArgsConstructor
public class ChangePostMessageProcessor extends MessageEventPublisher<ChangePostMessage>
    implements MessageProcessor<ChangePostMessage> {
  private final PostRepository postRepository;

  @Override
  public void process(ChangePostMessage message) {
    runSelectionSpecificLogic(message.getData());
    message.getData().setId(message.getAffectedMessageId());
    postRepository.save(message.getData());
    publish(message);
  }
}
