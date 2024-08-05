package com.coral.oxygen.middleware.common.configuration;

import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver;
import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

/**
 * This class shouldn't be marked with @Configuration as the 2 classes which inherit from them
 * already have @Configuration. Adding @Configuration here implies that inherited classes will
 * override (with the same values) bean definitions defined in this class. Bean overriding has been
 * disabled from Spring Boot 2.1 (can be enabled via config but is not recommended, as it causes
 * hard to find bugs).
 */
public class KafkaConfiguration {

  protected static final short MIN_NUM_PARTITIONS = 1;

  private String kafkaBrokers;
  protected Integer defaultNumPartitions;
  protected short replicaFactor;
  protected TopicResolver topicResolver;

  public KafkaConfiguration(
      @Value("${spring.kafka.bootstrap-servers}") String kafkaBrokers,
      @Value("${kafka.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.replica.factor}") short replicaFactor,
      TopicResolver topicResolver) {
    this.kafkaBrokers = kafkaBrokers;
    this.defaultNumPartitions = defaultNumPartitions;
    this.replicaFactor = replicaFactor;
    this.topicResolver = topicResolver;
  }

  @Bean
  public ProducerFactory<String, String> producerFactory() {
    return new DefaultKafkaProducerFactory<>(producerConfigs());
  }

  @Bean
  public Map<String, Object> producerConfigs() {
    Map<String, Object> props = new HashMap<>();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBrokers);
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    // See https://kafka.apache.org/documentation/#producerconfigs for more properties
    return props;
  }

  @Bean
  public KafkaTemplate<String, String> kafkaTemplate() {
    return new KafkaTemplate<>(producerFactory());
  }

  @Bean
  public KafkaAdmin admin() {
    Map<String, Object> configs = new HashMap<>();
    configs.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBrokers);
    return new KafkaAdmin(configs);
  }

  @Bean
  public AdminClient adminClient() {
    Map<String, Object> configs = new HashMap<>();
    configs.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBrokers);
    return AdminClient.create(configs);
  }
}
