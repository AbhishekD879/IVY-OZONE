package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.config.InternalKafkaProperties.TopicProperties;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.common.config.TopicConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@Configuration
@EnableKafka
@EnableConfigurationProperties
public class InternalKafkaConfig {

  @Value("${internal.listenersConcurrency:1}")
  private int listenerConcurrency;

  @Bean
  public KafkaAdmin kafkaAdmin(InternalKafkaProperties internalKafkaProperties) {
    return new KafkaAdmin(internalKafkaProperties.getKafka().getAdmin().buildProperties());
  }

  private NewTopic getTopicFromConfig(InternalKafkaProperties kafkaProperties, String topicName) {
    TopicProperties topicProperties = kafkaProperties.getTopics().get(topicName);

    return TopicBuilder.name(topicName)
        .partitions(topicProperties.getPartitions())
        .replicas(topicProperties.getReplica())
        .compact()
        .config(
            TopicConfig.RETENTION_MS_CONFIG,
            String.valueOf(kafkaProperties.getRetention().toMillis()))
        .config(
            TopicConfig.CLEANUP_POLICY_CONFIG,
            TopicConfig.CLEANUP_POLICY_DELETE + "," + TopicConfig.CLEANUP_POLICY_COMPACT)
        .build();
  }

  private <T>
      KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, T>>
          createKafkaListenerContainer(InternalKafkaProperties internalKafkaProperties) {
    ConcurrentKafkaListenerContainerFactory<String, T> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConcurrency(listenerConcurrency);
    DefaultKafkaConsumerFactory<String, T> consumerFactory =
        new DefaultKafkaConsumerFactory<>(
            internalKafkaProperties.getKafka().getConsumer().buildProperties());
    factory.setConsumerFactory(consumerFactory);
    return factory;
  }

  @Bean
  public KafkaTemplate<String, Object> internalKafkaTemplate(
      InternalKafkaProperties internalKafkaProperties) {
    return new KafkaTemplate<>(
        new DefaultKafkaProducerFactory<>(
            internalKafkaProperties.getKafka().getProducer().buildProperties()));
  }

  @Bean
  public NewTopic payoutUpdatesTopic(InternalKafkaProperties kafkaProperties) {
    return getTopicFromConfig(kafkaProperties, InternalKafkaTopics.PAYOUT_UDPATES.getTopicName());
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, Object>>
      kafkaPayoutUpdateContainerFactory(InternalKafkaProperties internalKafkaProperties) {
    return createKafkaListenerContainer(internalKafkaProperties);
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, Object>>
      kafkaEventUpdateContainerFactory(InternalKafkaProperties internalKafkaProperties) {
    return createKafkaListenerContainer(internalKafkaProperties);
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, Object>>
      kafkaTwoUpUpdateContainerFactory(InternalKafkaProperties internalKafkaProperties) {
    return createKafkaListenerContainer(internalKafkaProperties);
  }
}
