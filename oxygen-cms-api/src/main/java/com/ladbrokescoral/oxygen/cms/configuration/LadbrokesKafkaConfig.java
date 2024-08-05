package com.ladbrokescoral.oxygen.cms.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.google.common.collect.ImmutableMap;
import com.ladbrokescoral.oxygen.cms.api.dto.PromoMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.common.config.TopicConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.serializer.JsonSerializer;

@Profile("!UNIT")
@Configuration
@EnableKafka
@EnableConfigurationProperties
public class LadbrokesKafkaConfig {

  private LadbrokesKafkaProperties ladbrokesKafkaProperties;

  @Value(value = "${ladbrokes.kafka.topic.leaderboard-contest}")
  private String leaderboardContestTopic;

  @Value(value = "${ladbrokes.kafka.topic.leaderboard-promo}")
  private String leaderboardPromoTopic;

  @Value(value = "${ladbrokes.topic.timeline}")
  private String ladsTimelineTopic;

  @Value(value = "${ladbrokes.kafka.partitions}")
  private int ladsPartitions;

  @Value(value = "${ladbrokes.kafka.replicaFactor}")
  private short replicaFactor;

  public LadbrokesKafkaConfig(LadbrokesKafkaProperties ladbrokesKafkaProperties) {
    this.ladbrokesKafkaProperties = ladbrokesKafkaProperties;
  }

  @Bean(name = "ladbrokesKafkaAdmin")
  public KafkaAdmin admin() {
    return new KafkaAdmin(ladbrokesKafkaProperties.getKafka().buildAdminProperties());
  }

  @Bean(name = "ladbrokesAdminClient")
  public AdminClient adminClient() {
    return AdminClient.create(ladbrokesKafkaProperties.getKafka().buildAdminProperties());
  }

  @Bean
  public NewTopic contestTopic() {
    return new NewTopic(leaderboardContestTopic, ladsPartitions, replicaFactor)
        .configs(
            ImmutableMap.of(
                TopicConfig.RETENTION_MS_CONFIG, "-1",
                TopicConfig.RETENTION_BYTES_CONFIG, "-1"));
  }

  @Bean
  public NewTopic ladsTimelineTopic() {
    return new NewTopic(ladsTimelineTopic, ladsPartitions, replicaFactor)
        .configs(
            ImmutableMap.of(
                TopicConfig.RETENTION_MS_CONFIG, "-1",
                TopicConfig.RETENTION_BYTES_CONFIG, "-1"));
  }

  @Bean
  public ProducerFactory<String, String> ladbrokesProducerFactory() {
    DefaultKafkaProducerFactory<String, String> ladbrokesProducerFactory =
        new DefaultKafkaProducerFactory<>(
            ladbrokesKafkaProperties.getKafka().getProducer().buildProperties());
    ladbrokesProducerFactory.setKeySerializer(new StringSerializer());
    ladbrokesProducerFactory.setValueSerializer(new StringSerializer());
    return ladbrokesProducerFactory;
  }

  @Bean
  public NewTopic leaderboardPromoTopic() {
    return new NewTopic(leaderboardPromoTopic, ladsPartitions, replicaFactor);
  }

  @Bean
  public ProducerFactory<String, PromoMessageDto> promoLeaderboardProducerFactory() {
    DefaultKafkaProducerFactory<String, PromoMessageDto> producerFactory =
        new DefaultKafkaProducerFactory<>(
            ladbrokesKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  @Bean
  public KafkaTemplate<String, PromoMessageDto> promoLeaderboardKafkaTemplate() {
    return new KafkaTemplate<>(promoLeaderboardProducerFactory());
  }

  @Bean("ladbrokesKafkaTemplate")
  public KafkaTemplate<String, String> ladbrokesKafkaTemplate() {
    return new KafkaTemplate<>(ladbrokesProducerFactory());
  }

  @Bean
  public ProducerFactory<String, TimelineMessageDto> ladsTimelineProducerFactory() {
    DefaultKafkaProducerFactory<String, TimelineMessageDto> producerFactory =
        new DefaultKafkaProducerFactory<>(
            ladbrokesKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  @Bean
  public ProducerFactory<String, TimelineConfigDto> ladsTimelineProducerConfigFactory() {
    DefaultKafkaProducerFactory<String, TimelineConfigDto> producerFactory =
        new DefaultKafkaProducerFactory<>(
            ladbrokesKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  @Bean
  public KafkaTemplate<String, TimelineMessageDto> ladsTimelineKafkaTemplate() {
    return new KafkaTemplate<>((ladsTimelineProducerFactory()));
  }

  @Bean
  public KafkaTemplate<String, TimelineConfigDto> ladsTimelineKafkaConfigTemplate() {
    return new KafkaTemplate<>(ladsTimelineProducerConfigFactory());
  }

  private ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }
}
