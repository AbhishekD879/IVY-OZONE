package com.entain.oxygen.promosandbox.config;

import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@Configuration
@EnableKafka
@EnableConfigurationProperties
public class KafkaConsumerConfig {

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      kafkaInternalPromoConfigListenerContainerFactory(
          PromoSandboxKafkaProperties kafkaProperties) {
    return createKafkaListenerContainer(kafkaProperties);
  }

  private KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      createKafkaListenerContainer(PromoSandboxKafkaProperties kafkaProperties) {
    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    Map<String, Object> configs = new HashMap<>(kafkaProperties.getKafka().buildAdminProperties());
    configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    factory.setConsumerFactory(new DefaultKafkaConsumerFactory<>(configs));
    return factory;
  }
}
