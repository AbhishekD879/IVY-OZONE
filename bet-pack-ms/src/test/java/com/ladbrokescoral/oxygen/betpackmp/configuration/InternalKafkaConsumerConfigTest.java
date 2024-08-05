package com.ladbrokescoral.oxygen.betpackmp.configuration;

import java.util.List;
import java.util.Map;
import org.apache.kafka.clients.admin.NewTopic;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@ExtendWith(MockitoExtension.class)
class InternalKafkaConsumerConfigTest implements WithAssertions {

  private final String bootstrapServers = "localhost:9092";
  private final String subscriptionTopicName = "bet-pack-subscription-topic";
  private Integer defaultNumPartitions = 1;
  private short replicaFactor = 1;

  @InjectMocks
  private InternalKafkaConsumerConfig kafkaConsumerConfig =
      new InternalKafkaConsumerConfig(
          bootstrapServers, subscriptionTopicName, defaultNumPartitions, replicaFactor);

  @Test
  void subscriptionTopic() {
    NewTopic topic = kafkaConsumerConfig.betPackSubscriptionTopic();
    Assertions.assertNotNull(topic);
  }

  @Test
  void consumerConfigs() {
    Map<String, Object> result = kafkaConsumerConfig.consumerConfigs();
    Assertions.assertNotNull(result);
  }

  @Test
  void consumerFactory() {
    ConsumerFactory<String, String> result = kafkaConsumerConfig.consumerFactory();
    Assertions.assertNotNull(result);
  }

  @Test
  void internalBetPackKafkaFactory() {
    KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>> result =
        kafkaConsumerConfig.internalBetPackKafkaFactory("groupId", 5);
    Assertions.assertNotNull(result);
  }

  @Test
  void internalCmsActiveBetPacksKafkaFactory() {
    KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, List<String>>> result =
        kafkaConsumerConfig.internalCmsActiveBetPacksKafkaFactory("groupId", 5);
    Assertions.assertNotNull(result);
  }
}
