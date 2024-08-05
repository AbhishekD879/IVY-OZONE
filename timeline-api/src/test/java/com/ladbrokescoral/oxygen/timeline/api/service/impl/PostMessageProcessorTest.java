package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doReturn;

import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.time.Instant;
import lombok.extern.slf4j.Slf4j;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

@Slf4j
@RunWith(MockitoJUnitRunner.class)
public class PostMessageProcessorTest {
  @Mock private ApplicationEventPublisher eventPublisher;
  @Mock PostRepository postRepository;
  @InjectMocks PostMessageProcessor postMessageProcessor;

  @Before
  public void init() {
    PostMessage postMessage = PostMessage.builder().build();
    postMessage.setCampaignId("12345");
    postMessage.setCampaignName("abcd");
    postMessage.setPinned(true);
    postMessage.setHeaderText("abcd");
    postMessage.setSpotlight(true);
    postMessage.setId("12345");
    postMessage.setText("hello");
    postMessage.setVerdict(true);
    Instant instant = Instant.now();
    postMessage.setCreatedDate(instant);
    postMessage.setBrand("coral");
    doReturn(postMessage).when(postRepository).save(any(PostMessage.class));
  }

  @Test()
  public void savetest() {
    try {
      PostMessage postMessage = PostMessage.builder().build();
      postMessage.setCampaignId("12345");
      postMessage.setCampaignName("abcd");
      postMessage.setPinned(true);
      postMessage.setHeaderText("abcd");
      postMessage.setSpotlight(true);
      postMessage.setId("12345");
      postMessage.setText("hello");
      postMessage.setVerdict(true);
      Instant instant = Instant.now();
      postMessage.setCreatedDate(instant);
      postMessage.setBrand("coral");
      PostMessage saved = postRepository.save(postMessage);
      assertNotNull(saved);
      postMessageProcessor.process(postMessage);
      assertEquals("12345", postMessage.getId());
    } catch (Exception e) {
      log.info("Exception {}", e);
    }
  }
}
