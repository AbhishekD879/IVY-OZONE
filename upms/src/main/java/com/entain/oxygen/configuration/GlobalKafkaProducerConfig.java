package com.entain.oxygen.configuration;

import com.entain.oxygen.util.KafkaConstant;
import java.util.Map;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.RoundRobinAssignor;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

@Configuration
@EnableKafka
@EnableConfigurationProperties
@ConditionalOnProperty(value = "upms_kafka.enabled", havingValue = "true", matchIfMissing = true)
public class GlobalKafkaProducerConfig {

  @Autowired private GlobalKafkaProperties globalKafkaProperties;

  @Bean
  public KafkaTemplate<String, String> globalKafkaTemplate() {
    return new KafkaTemplate<>(globalKafkaProducerFactory());
  }

  private ProducerFactory<String, String> globalKafkaProducerFactory() {
    globalKafkaProperties.getKafka().buildProducerProperties();
    Map<String, Object> configProps = globalKafkaProperties.getKafka().buildProducerProperties();
    configProps.put(
        KafkaConstant.SSL_ENABLED_PROTOCOLS.value(),
        KafkaConstant.SSL_ENABLED_PROTOCOLS_VERSIONS.value());
    configProps.put(
        KafkaConstant.SSL_ENDPOINT_IDENTIFICATION_ALGORITHM.value(),
        KafkaConstant.EMPTY_STRING.value());
    configProps.put(
        ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, RoundRobinAssignor.class.getName());
    configProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    return new DefaultKafkaProducerFactory<>(configProps);
  }
}
