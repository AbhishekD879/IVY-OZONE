package com.ladbrokescoral.oxygen.cms.configuration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import java.util.List;
import org.apache.kafka.clients.admin.NewTopic;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.kafka.support.serializer.JsonSerializer;

@Profile("!UNIT")
@Configuration
@EnableKafka
@EnableConfigurationProperties
public class CmsPushLadbrokesKafkaConfig {

  private LadbrokesKafkaProperties ladbrokesKafkaProperties;
  private final LadbrokesSportsPageTopics sportsPageTopics;

  @Value(value = "${ladbrokes.kafka.partitions}")
  private int partitions;

  @Value(value = "${ladbrokes.kafka.replicaFactor}")
  private short replicaFactor;

  @Value(value = "${topic.lads.cms-push.partitions}")
  private int pushKafkaPartitions;

  @Value(value = "${topic.lads.cms-push.replicaFactor}")
  private short pushKafkaReplicaFactor;

  // Adding this properties for config-map details data publishing (CMS-PushMechanism)
  @Value(value = "${ladbrokes.kafka.topic.cms-config-map}")
  private String configMapTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-quiz}")
  private String quizTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-games}")
  private String gamesTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-season}")
  private String seasonTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-qualification-rule}")
  private String qualificationRule;

  @Value(value = "${ladbrokes.kafka.topic.cms-gamification}")
  private String gamificationTopic;

  public CmsPushLadbrokesKafkaConfig(
      LadbrokesKafkaProperties ladbrokesKafkaProperties,
      LadbrokesSportsPageTopics sportsPageTopics) {
    this.ladbrokesKafkaProperties = ladbrokesKafkaProperties;
    this.sportsPageTopics = sportsPageTopics;
  }

  @Bean
  public ProducerFactory<String, List<ApiCollectionConfig>> configMapProducerFactory() {
    DefaultKafkaProducerFactory<String, List<ApiCollectionConfig>> producerFactory =
        new DefaultKafkaProducerFactory<>(
            ladbrokesKafkaProperties.getKafka().getProducer().buildProperties());
    producerFactory.setKeySerializer(new StringSerializer());
    producerFactory.setValueSerializer(new JsonSerializer<>(objectMapper()));
    return producerFactory;
  }

  private ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }

  @Bean
  public KafkaTemplate<String, List<ApiCollectionConfig>> configMapKafkaTemplate() {
    return new KafkaTemplate<>(configMapProducerFactory());
  }

  @Bean
  public NewTopic configMapTopic() {
    return new NewTopic(configMapTopic, pushKafkaPartitions, pushKafkaReplicaFactor);
  }

  @Bean
  public NewTopic gamesTopic() {
    return new NewTopic(gamesTopic, partitions, replicaFactor);
  }

  @Bean
  public NewTopic seasonTopic() {
    return new NewTopic(seasonTopic, partitions, replicaFactor);
  }

  @Bean
  public NewTopic qualificationRuleTopic() {
    return new NewTopic(qualificationRule, partitions, replicaFactor);
  }

  @Bean
  public NewTopic quizTopic() {
    return new NewTopic(quizTopic, partitions, replicaFactor);
  }

  @Bean
  public NewTopic gamificationTopic() {
    return new NewTopic(gamificationTopic, partitions, replicaFactor);
  }

  @Bean
  public NewTopic sportsTopic() {
    return new NewTopic(sportsPageTopics.getSportsTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic sportCategoriesTopic() {
    return new NewTopic(sportsPageTopics.getSportcategoriesTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic moduleRibbontabsTopic() {
    return new NewTopic(sportsPageTopics.getModuleribbontabsTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic homeModulesTopic() {
    return new NewTopic(sportsPageTopics.getHomemodulesTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic sportQuicklinksTopic() {
    return new NewTopic(sportsPageTopics.getSportquicklinksTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic ycLeaguesTopic() {
    return new NewTopic(sportsPageTopics.getYcleaguesTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic systemConfigurationsTopic() {
    return new NewTopic(sportsPageTopics.getSystemconfigurationsTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic assetManagementTopic() {
    return new NewTopic(sportsPageTopics.getAssetmanagementTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic fanzonesTopic() {
    return new NewTopic(sportsPageTopics.getFanzonesTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic sportModulesTopic() {
    return new NewTopic(sportsPageTopics.getSportModulesTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic homeInplaySportTopic() {
    return new NewTopic(sportsPageTopics.getHomeInplaySportTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic sporttabsTopic() {
    return new NewTopic(sportsPageTopics.getSporttabsTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic surfaceBetTopic() {
    return new NewTopic(sportsPageTopics.getSurfaceBetTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic surfacebetArchiveTopic() {
    return new NewTopic(sportsPageTopics.getSurfacebetArchiveTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic highlightCarouselTopic() {
    return new NewTopic(sportsPageTopics.getHighlightCarouselTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic highlightCarouselArchiveTopic() {
    return new NewTopic(
        sportsPageTopics.getHighlightCarouselArchiveTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic segmentsTopic() {
    return new NewTopic(sportsPageTopics.getSegmentsTopic(), partitions, replicaFactor);
  }

  @Bean
  public NewTopic segmentedModulesTopic() {
    return new NewTopic(sportsPageTopics.getSegmentedModulesTopic(), partitions, replicaFactor);
  }
}
