package com.ladbrokescoral.cashout.config;

import static org.junit.Assert.assertNotNull;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;

@RunWith(MockitoJUnitRunner.class)
class ReactiveKafkaProducerConfigTest {
  private ReactiveKafkaProducerConfig reactiveKafkaProducerConfig;

  @BeforeEach
  public void init() {
    reactiveKafkaProducerConfig = new ReactiveKafkaProducerConfig();
  }

  @Test
  void testReactiveKafkaProducerTemplate() {
    InternalKafkaProperties properties = new InternalKafkaProperties();
    KafkaProperties props = new KafkaProperties();
    properties.setKafka(props);
    assertNotNull(reactiveKafkaProducerConfig.betDetailReactiveKafkaProducerTemplate(properties));
    assertNotNull(reactiveKafkaProducerConfig.cashoutReqReactiveKafkaProducerTemplate(properties));
    assertNotNull(reactiveKafkaProducerConfig.betUpdateReactiveKafkaProducerTemplate(properties));
    assertNotNull(
        reactiveKafkaProducerConfig.betUpdatesErrorReactiveKafkaProducerTemplate(properties));
  }
}
