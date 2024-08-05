package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import com.ladbrokescoral.oxygen.timeline.api.model.message.ChangePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.time.Instant;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

@Slf4j
@RunWith(MockitoJUnitRunner.class)
public class ChangePostMessageProcessorTest {
  @Mock ApplicationEventPublisher eventPublisher;
  @InjectMocks ChangePostMessageProcessor changePostMessageProcessor;
  @Mock PostRepository postRepository;

  @Test(expected = NullPointerException.class)
  public void savetest() {
    ChangePostMessage changePostMessage = new ChangePostMessage();
    changePostMessage.setId("12345");
    Instant instant = Instant.now();
    changePostMessage.setCreatedDate(instant);
    changePostMessage.setBrand("coral");
    changePostMessage.setAffectedMessageId("12345");
    changePostMessage.setCreatedDate(instant);
    changePostMessage.setAffectedMessageCreatedDate(instant);
    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCreatedDate(instant);
    changePostMessage.setData(postMessage);
    postRepository.save(changePostMessage.getData());
    changePostMessageProcessor.process(changePostMessage);
  }
}
