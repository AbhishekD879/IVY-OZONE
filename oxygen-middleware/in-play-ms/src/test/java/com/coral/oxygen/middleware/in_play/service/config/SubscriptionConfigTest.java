package com.coral.oxygen.middleware.in_play.service.config;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.integration.dsl.MessageChannels;
import org.springframework.messaging.SubscribableChannel;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@RunWith(MockitoJUnitRunner.class)
@SpringBootTest(classes = {SubscriptionConfig.class})
public class SubscriptionConfigTest {

  private SubscriptionConfig subscriptionConfig;

  @Mock private ThreadPoolTaskExecutor threadPoolTaskExecutor;

  @Mock private MessageChannels messageChannels;

  @Test
  public void messageChannel_shouldReturnSubscribableChannel() {

    subscriptionConfig = new SubscriptionConfig();
    SubscribableChannel expectedChannel = MessageChannels.publishSubscribe().get();
    SubscribableChannel actualChannel = subscriptionConfig.messageChannel(threadPoolTaskExecutor);

    assertNotNull(actualChannel);
    assertEquals(expectedChannel.getClass(), actualChannel.getClass());
  }
}
