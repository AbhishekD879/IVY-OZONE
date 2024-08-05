package com.coral.oxygen.middleware.ms.liveserv.configuration;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@EnableKafka
@ComponentScan("com.coral.oxygen.middleware.ms.liveserv")
@Configuration
public class KafkaConsumerConfig {

  private String bootstrapServers;
  private String subscriptionTopicName;
  protected Integer defaultNumPartitions;
  protected short replicaFactor;
  private Integer concurrencyListenersNum;

  public KafkaConsumerConfig(
      @Value("${spring.kafka.bootstrap-servers}") String bootstrapServers,
      @Value("${topic.subscription}") String subscriptionTopicName,
      @Value("${kafka.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.replica.factor}") short replicaFactor,
      @Value("${kafka.listeners.number}") Integer concurrencyListenersNum) {
    this.bootstrapServers = bootstrapServers;
    this.subscriptionTopicName = subscriptionTopicName;
    this.defaultNumPartitions = defaultNumPartitions;
    this.replicaFactor = replicaFactor;
    this.concurrencyListenersNum = concurrencyListenersNum;
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
      kafkaSubscriptionListenerContainerFactory() {
    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(consumerFactory());
    factory.setConcurrency(concurrencyListenersNum);
    return factory;
  }

  @Bean
  public NewTopic subscriptionTopic() {
    return new NewTopic(subscriptionTopicName, defaultNumPartitions, replicaFactor);
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      internalDFKafkaFactory(
          @Value("${internal.df.kafka.groupId}") String groupId,
          @Value("${internal.df.kafka.listenersConcurrency}") Integer listenersConcurrency) {
    Map<String, Object> configs = new HashMap<>(consumerConfigs());
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);

    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(new DefaultKafkaConsumerFactory<>(configs));
    factory.setConcurrency(listenersConcurrency);
    return factory;
  }

  @Bean
  public NewTopic internalDfUpdatesTopic(
      @Value("${topic.internal.df.scoreboards}") String topicName,
      @Value("${internal.df.kafka.partitions}") Integer partitionsCount) {
    return new NewTopic(topicName, partitionsCount, replicaFactor);
  }
}
