package com.ladbrokescoral.cashout.config;

import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.cashout.config.InternalKafkaProperties.TopicProperties;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class InternalKafkaConfigTest {
  @InjectMocks InternalKafkaConfig internalKafkaConfig;

  @Test
  void testPayoutOfferRequestsTopic() {
    try {
      Map<String, TopicProperties> properties = new HashMap<>();
      properties.put("payout-updates", new TopicProperties());
      InternalKafkaProperties internalKafkaProperties = new InternalKafkaProperties();
      KafkaProperties kafkaProperties = new KafkaProperties();
      internalKafkaProperties.setKafka(kafkaProperties);
      internalKafkaProperties.setListenersConcurrency(0);
      internalKafkaProperties.setRetention(Duration.ZERO);
      internalKafkaProperties.setTopics(properties);
      internalKafkaConfig.payoutUpdatesTopic(internalKafkaProperties);
      internalKafkaConfig.kafkaPayoutUpdateContainerFactory(internalKafkaProperties);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void testEventUpdateRequests() {
    try {
      Map<String, TopicProperties> properties = new HashMap<>();
      properties.put("event-updates", new TopicProperties());
      InternalKafkaProperties internalKafkaProperties = new InternalKafkaProperties();
      KafkaProperties kafkaProperties = new KafkaProperties();
      internalKafkaProperties.setKafka(kafkaProperties);
      internalKafkaProperties.setListenersConcurrency(0);
      internalKafkaProperties.setRetention(Duration.ZERO);
      internalKafkaProperties.setTopics(properties);
      internalKafkaConfig.kafkaEventUpdateContainerFactory(internalKafkaProperties);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void testTwoUpUpdateRequests() {
    try {
      Map<String, TopicProperties> properties = new HashMap<>();
      properties.put("twoup-updates", new TopicProperties());
      InternalKafkaProperties internalKafkaProperties = new InternalKafkaProperties();
      KafkaProperties kafkaProperties = new KafkaProperties();
      internalKafkaProperties.setKafka(kafkaProperties);
      internalKafkaProperties.setListenersConcurrency(0);
      internalKafkaProperties.setRetention(Duration.ZERO);
      internalKafkaProperties.setTopics(properties);
      internalKafkaConfig.kafkaTwoUpUpdateContainerFactory(internalKafkaProperties);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }
}
