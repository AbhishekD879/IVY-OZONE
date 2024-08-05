package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
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
import org.springframework.kafka.support.serializer.JsonSerializer;

@Configuration
public class InternalKafkaProducerConfig {

  private String kafkaBrokers;
  private String betPackUpdatesTopicName;
  protected Integer defaultNumPartitions;
  protected short replicaFactor;

  public InternalKafkaProducerConfig(
      @Value("${spring.kafka.bootstrap-servers}") String kafkaBrokers,
      @Value("${topic.bet-pack-live-updates}") String betPackUpdatesTopicName,
      @Value("${kafka.bet-pack-live-updates.partition.default}") Integer defaultNumPartitions,
      @Value("${kafka.bet-pack-live-updates.replica.factor}") short replicaFactor) {
    this.kafkaBrokers = kafkaBrokers;
    this.betPackUpdatesTopicName = betPackUpdatesTopicName;
    this.defaultNumPartitions = defaultNumPartitions;
    this.replicaFactor = replicaFactor;
  }

  @Bean
  public ProducerFactory<String, FreebetOffer> producerFactory() {
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
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
    return props;
  }

  @Bean
  public NewTopic liveUpdatesTopic() {
    return new NewTopic(betPackUpdatesTopicName, defaultNumPartitions, replicaFactor);
  }

  @Bean
  public KafkaTemplate<String, FreebetOffer> kafkaTemplate() {
    return new KafkaTemplate<>(producerFactory());
  }
}
