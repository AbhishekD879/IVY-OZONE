package com.ladbrokescoral.cashout.config;

import static org.junit.Assert.assertNotNull;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import reactor.kafka.receiver.ReceiverOptions;

@RunWith(MockitoJUnitRunner.class)
class SafBafConsumerConfigTest {
  private SafBafConsumerConfig safBafConsumerConfig;
  @Mock private ReceiverOptions<String, String> receiverOptions;

  @BeforeEach
  public void init() {
    safBafConsumerConfig = new SafBafConsumerConfig();
    receiverOptions = ReceiverOptions.create();
  }

  @Test
  void testkafkaReceiverOptions() {
    InternalKafkaProperties properties = new InternalKafkaProperties();
    DfKafkaProperties props = new DfKafkaProperties();
    KafkaProperties config = new KafkaProperties();
    props.setKafka(config);
    properties.setKafka(props.getKafka());
    safBafConsumerConfig.buildGroupId("1", "cashout", "23");
    assertNotNull(safBafConsumerConfig.basicReceiverOptions(props));
  }

  @Test
  void testBafUpdatesListenerTemplate() {
    assertNotNull(safBafConsumerConfig.bafUpdatesListenerTemplate(receiverOptions));
    assertNotNull(safBafConsumerConfig.safUpdatesListenerTemplate(receiverOptions));
  }
}
