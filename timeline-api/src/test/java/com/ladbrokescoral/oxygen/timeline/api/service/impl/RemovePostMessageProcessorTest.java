package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.timeline.api.model.message.RemovePostMessage;
import com.ladbrokescoral.oxygen.timeline.api.repository.PostRepository;
import java.time.Instant;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.test.context.ContextConfiguration;

@SpringBootTest(classes = RemovePostMessageProcessor.class)
@ContextConfiguration(classes = RemovePostMessageProcessorTest.MockitoPublisherConfiguration.class)
@RunWith(MockitoJUnitRunner.class)
public class RemovePostMessageProcessorTest {
  @Mock private ApplicationEventPublisher eventPublisher;
  @InjectMocks RemovePostMessageProcessor removePostMessageProcessor;
  @Mock private PostRepository postRepository;
  @Mock RemovePostMessage removePostMessage1;

  @Before
  public void init() {
    doNothing().when(postRepository).deleteById(any(String.class));
    RemovePostMessage removePostMessage = new RemovePostMessage();
    removePostMessage.setBrand("coral");
    removePostMessage.setAffectedMessageId("12345");
    Instant instant = Instant.now();
    removePostMessage.setCreatedDate(instant);
    removePostMessage.setId("12345");
    removePostMessage.setAffectedMessageCreatedDate(instant);
  }

  @Test(expected = NullPointerException.class)
  public void deleteMethod() {
    RemovePostMessage removePostMessage = new RemovePostMessage();
    removePostMessage.setBrand("coral");
    removePostMessage.setAffectedMessageId("12345");
    Instant instant = Instant.now();
    removePostMessage.setCreatedDate(instant);
    removePostMessage.setId("12345");
    removePostMessage.setAffectedMessageCreatedDate(instant);
    removePostMessage1 = removePostMessage;
    removePostMessageProcessor.process(removePostMessage1);
  }

  @TestConfiguration
  static class MockitoPublisherConfiguration {

    @Bean
    @Primary
    ApplicationEventPublisher publisher() {
      return mock(ApplicationEventPublisher.class);
    }
  }
}
