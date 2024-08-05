package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.entity.ApiCollectionConfig;
import java.util.List;
import org.apache.kafka.clients.admin.NewTopic;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.test.util.ReflectionTestUtils;

public class CmsPushLadbrokesKafkaConfigTest {

  @InjectMocks private CmsPushLadbrokesKafkaConfig ladbrokesKafkaConfig;

  @Before
  public void init() throws NoSuchFieldException, IllegalAccessException {
    LadbrokesKafkaProperties ladbrokesKafkaProperties = new LadbrokesKafkaProperties();
    LadbrokesSportsPageTopics sportsPageTopics = new LadbrokesSportsPageTopics();
    ladbrokesKafkaProperties.setKafka(new KafkaProperties());
    ladbrokesKafkaConfig =
        new CmsPushLadbrokesKafkaConfig(ladbrokesKafkaProperties, sportsPageTopics);
    ReflectionTestUtils.setField(
        ladbrokesKafkaConfig, "ladbrokesKafkaProperties", ladbrokesKafkaProperties);
    ReflectionTestUtils.setField(ladbrokesKafkaConfig, "partitions", 1);
    ReflectionTestUtils.setField(ladbrokesKafkaConfig, "replicaFactor", (short) 1);
    ReflectionTestUtils.setField(ladbrokesKafkaConfig, "configMapTopic", "configMap-topic");
  }

  @Test
  public void testConfigMapProducerFactory() {
    ProducerFactory<String, List<ApiCollectionConfig>> factory =
        ladbrokesKafkaConfig.configMapProducerFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  public void testConfigMapKafkaTemplate() {
    KafkaTemplate<String, List<ApiCollectionConfig>> kafkaConfigTemplate =
        ladbrokesKafkaConfig.configMapKafkaTemplate();
    Assert.assertNotNull(kafkaConfigTemplate);
  }

  @Test
  public void testConfigMapTopic() {
    NewTopic topic = ladbrokesKafkaConfig.configMapTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testGamesTopic() {
    NewTopic topic = ladbrokesKafkaConfig.gamesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSportsTopic() {
    NewTopic topic = ladbrokesKafkaConfig.sportsTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSportCategoriesTopic() {
    NewTopic topic = ladbrokesKafkaConfig.sportCategoriesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testModuleribbontabsTopic() {
    NewTopic topic = ladbrokesKafkaConfig.moduleRibbontabsTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testHomemodulesTopic() {
    NewTopic topic = ladbrokesKafkaConfig.homeModulesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSportquicklinksTopic() {
    NewTopic topic = ladbrokesKafkaConfig.sportQuicklinksTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testYcleaguesTopic() {
    NewTopic topic = ladbrokesKafkaConfig.ycLeaguesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSystemconfigurationsTopic() {
    NewTopic topic = ladbrokesKafkaConfig.systemConfigurationsTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testAssetManagementTopic() {
    NewTopic topic = ladbrokesKafkaConfig.assetManagementTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testFanzonesTopic() {
    NewTopic topic = ladbrokesKafkaConfig.fanzonesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSportModulesTopic() {
    NewTopic topic = ladbrokesKafkaConfig.sportModulesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testHomeInplaySportTopic() {
    NewTopic topic = ladbrokesKafkaConfig.homeInplaySportTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSportTabTopic() {
    NewTopic topic = ladbrokesKafkaConfig.sporttabsTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSurfaceBetTopic() {
    NewTopic topic = ladbrokesKafkaConfig.surfaceBetTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSATopic() {
    NewTopic topic = ladbrokesKafkaConfig.surfacebetArchiveTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testHCTopic() {
    NewTopic topic = ladbrokesKafkaConfig.highlightCarouselTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testHCArchiveTopic() {
    NewTopic topic = ladbrokesKafkaConfig.highlightCarouselArchiveTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSegmentTopic() {
    NewTopic topic = ladbrokesKafkaConfig.segmentsTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSegModuleTopic() {
    NewTopic topic = ladbrokesKafkaConfig.segmentedModulesTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testSeasonTopic() {
    NewTopic topic = ladbrokesKafkaConfig.seasonTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testQualificationRuleTopic() {
    NewTopic topic = ladbrokesKafkaConfig.qualificationRuleTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testQuizTopic() {
    NewTopic topic = ladbrokesKafkaConfig.quizTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testGamificationTopic() {
    NewTopic topic = ladbrokesKafkaConfig.gamificationTopic();
    Assert.assertNotNull(topic);
  }
}
