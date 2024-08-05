package com.ladbrokescoral.oxygen.timeline.api.config;

import static org.junit.Assert.assertNotNull;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class MessageProcessorConfigurationTest {

  @InjectMocks private MessageProcessorConfiguration messageProcessorConfiguration;

  @Test
  public void messageProcessorsTest() {
    messageProcessorConfiguration.messageProcessors();
    assertNotNull(messageProcessorConfiguration.messageProcessors());
  }
}
