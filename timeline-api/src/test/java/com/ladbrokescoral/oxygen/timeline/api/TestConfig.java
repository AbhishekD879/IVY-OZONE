package com.ladbrokescoral.oxygen.timeline.api;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.timeline.api.controller.MessageListener;
import com.ladbrokescoral.oxygen.timeline.api.controller.MessageProcessorFactory;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Profile;

@Profile("test")
@TestConfiguration
public class TestConfig {

  // @Bean
  MessageProcessorFactory messageProcessors() {
    MessageProcessorFactory mock = mock(MessageProcessorFactory.class);
    when(mock.getInstance(PostMessage.class)).thenReturn(null); // todo think about that,
    return mock;
  }

  // @Bean
  // @Primary
  MessageListener messageListener() {
    return mock(MessageListener.class);
  }

  // @Bean
  /*  public SocketIOServer socketIOServer() {
    return mock(SocketIOServer.class);
  }*/

  @Bean
  public InitListener initListener() {
    return mock(InitListener.class);
  }
}
