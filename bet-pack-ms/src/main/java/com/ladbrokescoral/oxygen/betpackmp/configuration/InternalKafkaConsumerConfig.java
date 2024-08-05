package com.ladbrokescoral.oxygen.betpackmp.configuration;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;
import org.springframework.kafka.support.serializer.JsonDeserializer;

@EnableKafka
@Configuration
public class InternalKafkaConsumerConfig {

  private String bootstrapServers;
  private String betPackSubscriptionTopicName;
  protected Integer defaultNumPartitions;
  protected short replicaFactor;

  public InternalKafkaConsumerConfig(
      @Value("${spring.kafka.bootstrap-servers}") String bootstrapServers,
      @Value("${topic.bet-pack-subscription}") String betPackSubscriptionTopicName,
      @Value("${kafka.bet-pack-subscription.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.bet-pack-subscription.replica.factor}") short replicaFactor) {
    this.bootstrapServers = bootstrapServers;
    this.betPackSubscriptionTopicName = betPackSubscriptionTopicName;
    this.defaultNumPartitions = defaultNumPartitions;
    this.replicaFactor = replicaFactor;
  }

  @Bean
  public Map<String, Object> consumerConfigs() {
    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    props.put(ConsumerConfig.GROUP_ID_CONFIG, UUID.randomUUID().toString());
    props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
    return props;
  }

  @Bean
  public ConsumerFactory<String, String> consumerFactory() {
    return new DefaultKafkaConsumerFactory<>(consumerConfigs());
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      internalBetPackKafkaFactory(
          @Value("${internal.bet-pack.kafka.groupId}") String groupId,
          @Value("${internal.bet-pack.kafka.listenersConcurrency}") Integer listenersConcurrency) {
    Map<String, Object> configs = new HashMap<>(consumerConfigs());
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);

    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(new DefaultKafkaConsumerFactory<>(configs));
    factory.setConcurrency(listenersConcurrency);
    return factory;
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, List<String>>>
      internalCmsActiveBetPacksKafkaFactory(
          @Value("${internal.active.bet-pack-ids.kafka.groupId}") String groupId,
          @Value("${internal.active.bet-pack-ids.kafka.listenersConcurrency}")
              Integer listenersConcurrency) {
    Map<String, Object> configs = new HashMap<>(consumerConfigs());
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
    ConcurrentKafkaListenerContainerFactory<String, List<String>> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(new DefaultKafkaConsumerFactory<>(configs));
    factory.setConcurrency(listenersConcurrency);
    return factory;
  }

  @Bean
  public NewTopic betPackSubscriptionTopic() {
    return new NewTopic(betPackSubscriptionTopicName, defaultNumPartitions, replicaFactor);
  }
}
