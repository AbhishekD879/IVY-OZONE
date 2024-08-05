package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import java.util.List;
import org.assertj.core.api.WithAssertions;
import org.junit.Assert;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class CmsPushBmaKafkaConfigTest implements WithAssertions {

  @InjectMocks private CmsPushBmaKafkaConfig kafkaProducerConfig;
  @Mock BmaSportsPageTopics bmaSportsPageTopics;

  @BeforeEach
  void setUp() {
    CoralKafkaProperties coralKafkaProperties = new CoralKafkaProperties();
    coralKafkaProperties.setKafka(new KafkaProperties());
    kafkaProducerConfig = new CmsPushBmaKafkaConfig(coralKafkaProperties, bmaSportsPageTopics);
    ReflectionTestUtils.setField(kafkaProducerConfig, "coralKafkaProperties", coralKafkaProperties);
    ReflectionTestUtils.setField(kafkaProducerConfig, "coralPartitions", 1);
    ReflectionTestUtils.setField(kafkaProducerConfig, "coralReplicaFactor", (short) 1);
    ReflectionTestUtils.setField(
        kafkaProducerConfig, "coralConfigMapTopic", "coral-cms-configMap-topic");
  }

  @Test
  void testConfigMapProducerFactory() {
    ProducerFactory<String, List<ApiCollectionConfig>> factory =
        kafkaProducerConfig.coralConfigMapProducerFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  void testConfigMapKafkaTemplate() {
    KafkaTemplate<String, List<ApiCollectionConfig>> coralConfigMapKafkaTemplate =
        kafkaProducerConfig.coralConfigMapKafkaTemplate();
    Assert.assertNotNull(coralConfigMapKafkaTemplate);
  }

  @Test
  void testCoralConfigMapTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralConfigMapTopic());
  }

  @Test
  void testCoralQuizTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralQuizTopic());
  }

  @Test
  void testCoralSportsTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSportsTopic());
  }

  @Test
  void testCoralSportCategoriesTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSportCategoriesTopic());
  }

  @Test
  void testCoralModuleRibbontabsTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralModuleRibbontabsTopic());
  }

  @Test
  void testCoralHomeModulesTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralHomeModulesTopic());
  }

  @Test
  void testCoralSportquicklinksTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSportQuicklinksTopic());
  }

  @Test
  void testCoralYcleaguesTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralYcleaguesTopic());
  }

  @Test
  void testCoralSystemconfigurationsTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSystemconfigurationsTopic());
  }

  @Test
  void testCoralAssetmanagementTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralAssetmanagementTopic());
  }

  @Test
  void testCoralFanzonesTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralFanzonesTopic());
  }

  @Test
  void testCoralSportModulesTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSportModulesTopic());
  }

  @Test
  void testCoralHomeInplaySportTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralHomeInplaySportTopic());
  }

  @Test
  void testCoralSportTabsTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSporttabsTopic());
  }

  @Test
  void testCoralSurfaceBetTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSurfaceBetTopic());
  }

  @Test
  void testCoralSurfacebetArchiveTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSurfacebetArchiveTopic());
  }

  @Test
  void testCoralHighlightCarouselTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralHighlightCarouselTopic());
  }

  @Test
  void testCoralHCATopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralHighlightCarouselArchiveTopic());
  }

  @Test
  void testCoralSegmentTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSegmentsTopic());
  }

  @Test
  void testCoralSMTopic() {
    Assert.assertNotNull(kafkaProducerConfig.coralSegmentedModulesTopic());
  }
}
