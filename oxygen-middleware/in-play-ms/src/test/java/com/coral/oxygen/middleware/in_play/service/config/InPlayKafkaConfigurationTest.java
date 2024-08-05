package com.coral.oxygen.middleware.in_play.service.config;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import org.apache.kafka.clients.admin.NewTopic;
import org.junit.Before;
import org.junit.Test;

public class InPlayKafkaConfigurationTest {

  private TopicResolver topicResolver;
  private static final String VIRTUAL_SPORTS_RIBBON_CHANGE = "VIRTUAL_SPORTS_RIBBON_CHANGED";
  private InPlayKafkaConfiguration inPlayKafkaConfiguration;

  @Before
  public void setUp() {

    topicResolver = mock(TopicResolver.class);
    inPlayKafkaConfiguration =
        new InPlayKafkaConfiguration("localhost:9092", 1, (short) 1, topicResolver);
  }

  @Test
  public void testVirtualSportsRibbonTopic() {
    when(topicResolver.find(any())).thenReturn(VIRTUAL_SPORTS_RIBBON_CHANGE);
    NewTopic topic = inPlayKafkaConfiguration.virtualSportsRibbonChangedTopic();
    assertNotNull(topic);
  }
}
