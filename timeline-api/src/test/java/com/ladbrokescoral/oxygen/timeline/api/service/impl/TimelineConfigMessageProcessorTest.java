package com.ladbrokescoral.oxygen.timeline.api.service.impl;

import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.oxygen.timeline.api.model.message.TimelineConfigMessage;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

@RunWith(MockitoJUnitRunner.class)
public class TimelineConfigMessageProcessorTest {

  @Mock private ApplicationEventPublisher eventPublisher;

  @InjectMocks private TimelineConfigMessageProcessor timelineConfigMessageProcessor;

  @Test
  public void testIfPostsWereSearchedWithProperId() {
    assertNotNull(timelineConfigMessageProcessor);
    timelineConfigMessageProcessor.process(TimelineConfigMessage.builder().enabled(true).build());
  }
}
