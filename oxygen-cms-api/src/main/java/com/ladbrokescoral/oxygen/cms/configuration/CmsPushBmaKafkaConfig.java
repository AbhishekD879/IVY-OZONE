package com.ladbrokescoral.oxygen.cms.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.serializer.JsonSerializer;

@Profile("!UNIT")
@Configuration
@EnableConfigurationProperties
@Slf4j
public class CmsPushBmaKafkaConfig {
  private final CoralKafkaProperties coralKafkaProperties;
  private static final String CORAL_KAFKASERVER = "coral kafka bootstrap servers:{}";
  private final BmaSportsPageTopics sportsPageTopics;

  public CmsPushBmaKafkaConfig(
      CoralKafkaProperties coralKafkaProperties, BmaSportsPageTopics sportsPageTopics) {
    this.coralKafkaProperties = coralKafkaProperties;
    this.sportsPageTopics = sportsPageTopics;
  }

  @Value(value = "${coral.kafka.partitions}")
  private int coralPartitions;

  @Value(value = "${coral.kafka.replicaFactor}")
  private short coralReplicaFactor;

  @Value(value = "${topic.coral.cms-push.partitions}")
  private int pushKafkaPartitions;

  @Value(value = "${topic.coral.cms-push.replicaFactor}")
  private short pushKafkaReplicaFactor;

  @Value(value = "${coral.kafka.topic.cms-config-map}")
  private String coralConfigMapTopic;

  @Value(value = "${coral.kafka.topic.cms-quiz}")
  private String coralQuizTopic;

  @Bean
  public ProducerFactory<String, List<ApiCollectionConfig>> coralConfigMapProducerFactory() {
    DefaultKafkaProducerFactory<String, List<ApiCollectionConfig>> producerFactory =
        new DefaultKafkaProducerFactory<>(
            coralKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setKeySerializer(new StringSerializer());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    log.info(CORAL_KAFKASERVER, coralKafkaProperties.getKafka().getProducer().buildProperties());
    return producerFactory;
  }

  @Bean
  public KafkaTemplate<String, List<ApiCollectionConfig>> coralConfigMapKafkaTemplate() {
    return new KafkaTemplate<>(coralConfigMapProducerFactory());
  }

  private ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }

  @Bean
  public NewTopic coralConfigMapTopic() {
    return new NewTopic(coralConfigMapTopic, pushKafkaPartitions, pushKafkaReplicaFactor);
  }

  @Bean
  public NewTopic coralQuizTopic() {
    return new NewTopic(coralQuizTopic, coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSportsTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSportsTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSportCategoriesTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSportcategoriesTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralModuleRibbontabsTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralModuleribbontabsTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralHomeModulesTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralHomemodulesTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSportQuicklinksTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSportquicklinksTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralYcleaguesTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralYcleaguesTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSystemconfigurationsTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSystemconfigurationsTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralAssetmanagementTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralAssetmanagementTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralFanzonesTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralFanzonesTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSportModulesTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSegmentedModulesTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralHomeInplaySportTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralHomeInplaySportTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSporttabsTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSporttabsTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSurfaceBetTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSurfaceBetTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSurfacebetArchiveTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSurfacebetArchiveTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralHighlightCarouselTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralHighlightCarouselTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralHighlightCarouselArchiveTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralHighlightCarouselArchiveTopic(),
        coralPartitions,
        coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSegmentsTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSegmentsTopic(), coralPartitions, coralReplicaFactor);
  }

  @Bean
  public NewTopic coralSegmentedModulesTopic() {
    return new NewTopic(
        sportsPageTopics.getCoralSegmentedModulesTopic(), coralPartitions, coralReplicaFactor);
  }
}
