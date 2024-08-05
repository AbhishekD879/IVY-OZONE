package com.entain.oxygen.configuration;

import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@ComponentScan("com.entain.oxygen")
@Configuration
@EnableKafka
@EnableConfigurationProperties
@ConditionalOnProperty(value = "upms_kafka.enabled", havingValue = "true", matchIfMissing = true)
public class KafkaConsumerConfig {

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      filteredKafkaContainerFactory(
          DfKafkaProperties dfKafkaProperties,
          @Value("${df.kafka.listenersConcurrency}") Integer listenersConcurrency) {

    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConcurrency(listenersConcurrency);

    DefaultKafkaConsumerFactory<String, String> consumerFactory =
        new DefaultKafkaConsumerFactory<>(
            dfKafkaProperties.getKafka().getConsumer().buildProperties());
    consumerFactory.setKeyDeserializer(new StringDeserializer());
    consumerFactory.setValueDeserializer(new StringDeserializer());
    factory.setConsumerFactory(consumerFactory);
    return factory;
  }
}
