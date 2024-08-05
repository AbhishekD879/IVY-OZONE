package com.ladbrokescoral.oxygen.configuration;

import com.ladbrokescoral.oxygen.model.FreebetOffer;
import org.apache.kafka.common.serialization.Deserializer;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class BetPackKafkaConsumerConfigTest {

  @InjectMocks private BetPackKafkaConsumerConfig betPackKafkaConsumerConfig;

  @BeforeEach
  void setUp() {
    ReflectionTestUtils.setField(betPackKafkaConsumerConfig, "bootstrapServers", "localhost:9092");
    ReflectionTestUtils.setField(betPackKafkaConsumerConfig, "kafkaConsumerCount", 6);
    ReflectionTestUtils.setField(betPackKafkaConsumerConfig, "betPackGroupId", "group_id");
  }

  @Test
  void kafkaBetPacksListenerContainerFactory() {
    KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, FreebetOffer>>
        containerFactory = betPackKafkaConsumerConfig.kafkaBetPacksListenerContainerFactory();
    Assertions.assertNotNull(containerFactory);
  }

  @Test
  void stringKeyDeserializer() {
    Deserializer<String> deserializer = betPackKafkaConsumerConfig.stringKeyDeserializer();
    Assertions.assertNotNull(deserializer);
  }

  @Test
  void betPackJsonValueDeserializer() {
    Deserializer<FreebetOffer> deserializer =
        betPackKafkaConsumerConfig.betPackJsonValueDeserializer();
    Assertions.assertNotNull(deserializer);
  }
}
