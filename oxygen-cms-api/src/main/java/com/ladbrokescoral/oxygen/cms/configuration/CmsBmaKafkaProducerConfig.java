package com.ladbrokescoral.oxygen.cms.configuration;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.google.common.collect.ImmutableMap;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.common.config.TopicConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.serializer.JsonSerializer;

@Profile("!UNIT")
@Configuration
@EnableConfigurationProperties
@Slf4j
public class CmsBmaKafkaProducerConfig {

  private final CoralKafkaProperties coralKafkaProperties;
  private static final String CORAL_KAFKASERVER = "coral kafka bootstrap servers:{}";

  @Value(value = "${coral.kafka.partitions}")
  private int coralPartitions;

  @Value(value = "${coral.kafka.replicaFactor}")
  private short coralReplicaFactor;

  @Value(value = "${coral.topic.active-bet-packs}")
  private String coralActiveBetPackTopic;

  @Value(value = "${coral.topic.timeline}")
  private String coralTimelineTopic;

  @Value(value = "${coral.kafka.topic.leaderboard-promo-coral}")
  private String leaderboardPromoCoralTopic;

  @Value(value = "${coral.topic.retention.ms}")
  private String retentionConfigMs;

  public CmsBmaKafkaProducerConfig(CoralKafkaProperties coralKafkaProperties) {
    this.coralKafkaProperties = coralKafkaProperties;
  }

  @Bean(name = "coralKafkaAdmin")
  public KafkaAdmin admin() {
    return new KafkaAdmin(coralKafkaProperties.getKafka().buildAdminProperties());
  }

  @Bean(name = "coralKafkaAdminClient")
  public AdminClient adminClient() {
    return AdminClient.create(coralKafkaProperties.getKafka().buildAdminProperties());
  }

  @Bean
  public NewTopic activeBetPackTopic() {
    return TopicBuilder.name(coralActiveBetPackTopic)
        .partitions(coralPartitions)
        .replicas(coralReplicaFactor)
        .compact()
        .config(TopicConfig.RETENTION_MS_CONFIG, retentionConfigMs)
        .config(
            TopicConfig.CLEANUP_POLICY_CONFIG,
            TopicConfig.CLEANUP_POLICY_DELETE + "," + TopicConfig.CLEANUP_POLICY_COMPACT)
        .build();
  }

  @Bean
  public ProducerFactory<String, List<String>> coralBetPackProducerFactory() {
    DefaultKafkaProducerFactory<String, List<String>> producerFactory =
        new DefaultKafkaProducerFactory<>(
            coralKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(new TypeReference<List<String>>() {}));
    log.info(CORAL_KAFKASERVER, coralKafkaProperties.getKafka().getProducer().buildProperties());
    return producerFactory;
  }

  @Bean
  public KafkaTemplate<String, List<String>> coralBetPackKafkaTemplate() {
    return new KafkaTemplate<>(coralBetPackProducerFactory());
  }

  @Bean
  public NewTopic coralTimelineTopic() {
    return new NewTopic(coralTimelineTopic, coralPartitions, coralReplicaFactor)
        .configs(
            ImmutableMap.of(
                TopicConfig.RETENTION_MS_CONFIG, "-1",
                TopicConfig.RETENTION_BYTES_CONFIG, "-1"));
  }

  @Bean
  public NewTopic leaderboardPromoCoralTopic() {
    return new NewTopic(leaderboardPromoCoralTopic, coralPartitions, coralReplicaFactor);
  }

  @Bean
  public ProducerFactory<String, PromoMessageDto> promoLeaderboardCoralProducerFactory() {
    DefaultKafkaProducerFactory<String, PromoMessageDto> producerFactory =
        new DefaultKafkaProducerFactory<>(
            coralKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  @Bean
  public ProducerFactory<String, TimelineMessageDto> producerFactory() {
    DefaultKafkaProducerFactory<String, TimelineMessageDto> producerFactory =
        new DefaultKafkaProducerFactory<>(
            coralKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  @Bean
  public ProducerFactory<String, TimelineConfigDto> producerConfigFactory() {
    DefaultKafkaProducerFactory<String, TimelineConfigDto> producerFactory =
        new DefaultKafkaProducerFactory<>(
            coralKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  @Bean
  public KafkaTemplate<String, TimelineMessageDto> kafkaTemplate() {
    return new KafkaTemplate<>(producerFactory());
  }

  @Bean
  public KafkaTemplate<String, TimelineConfigDto> kafkaConfigTemplate() {
    return new KafkaTemplate<>(producerConfigFactory());
  }

  @Bean
  public KafkaTemplate<String, PromoMessageDto> promoLeaderboardCoralKafkaTemplate() {
    return new KafkaTemplate<>(promoLeaderboardCoralProducerFactory());
  }

  private ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }

  @Bean
  public ProducerFactory<String, String> coralProducerFactory() {
    DefaultKafkaProducerFactory<String, String> producerFactory =
        new DefaultKafkaProducerFactory<>(
            coralKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setKeySerializer(new StringSerializer());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    log.info(CORAL_KAFKASERVER, coralKafkaProperties.getKafka().getProducer().buildProperties());
    return producerFactory;
  }

  @Bean
  public KafkaTemplate<String, String> coralKafkaTemplate() {
    return new KafkaTemplate<>(coralProducerFactory());
  }
}
