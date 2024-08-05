package com.coral.oxygen.middleware.ms.liveserv.configuration;

import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

@Configuration
public class KafkaProducerConfig {

  private String kafkaBrokers;
  private String liveUpdatesTopicName;
  private String scoreboardsTopic;
  protected Integer defaultNumPartitions;
  protected short replicaFactor;
  private String incidentsTopic;

  public KafkaProducerConfig(
      @Value("${spring.kafka.bootstrap-servers}") String kafkaBrokers,
      @Value("${topic.live-updates}") String liveUpdatesTopicName,
      @Value("${topic.scoreboards}") String scoreboardsTopic,
      @Value("${kafka.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.replica.factor}") short replicaFactor,
      @Value("${topic.incidents}") String incidentsTopic) {
    this.kafkaBrokers = kafkaBrokers;
    this.liveUpdatesTopicName = liveUpdatesTopicName;
    this.scoreboardsTopic = scoreboardsTopic;
    this.defaultNumPartitions = defaultNumPartitions;
    this.replicaFactor = replicaFactor;
    this.incidentsTopic = incidentsTopic;
  }

  @Bean
  public ProducerFactory<String, String> producerFactory() {
    return new DefaultKafkaProducerFactory<>(producerConfigs());
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

  @Bean
  public Map<String, Object> producerConfigs() {
    Map<String, Object> props = new HashMap<>();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBrokers);
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    return props;
  }

  @Bean
  public NewTopic liveUpdatesTopic() {
    return new NewTopic(liveUpdatesTopicName, defaultNumPartitions, replicaFactor);
  }

  @Bean
  public NewTopic scoreboardsTopic() {
    return new NewTopic(scoreboardsTopic, defaultNumPartitions, replicaFactor);
  }

  /**
   * This Method is used to create NewTopic for VAR Messages to publish LS Publisher
   *
   * @return NewTopic
   */
  @Bean
  public NewTopic incidentsTopic() {
    return new NewTopic(incidentsTopic, defaultNumPartitions, replicaFactor);
  }

  @Bean
  public KafkaTemplate<String, String> kafkaTemplate() {
    return new KafkaTemplate<>(producerFactory());
  }
}
