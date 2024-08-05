package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.test.util.ReflectionTestUtils;

public class LadbrokesKafkaConfigTest {

  private LadbrokesKafkaConfig ladbrokesKafkaConfig;

  @Before
  public void init() throws NoSuchFieldException, IllegalAccessException {
    LadbrokesKafkaProperties ladbrokesKafkaProperties = new LadbrokesKafkaProperties();
    ladbrokesKafkaProperties.setKafka(new KafkaProperties());
    ladbrokesKafkaConfig = new LadbrokesKafkaConfig(ladbrokesKafkaProperties);
    ReflectionTestUtils.setField(
        ladbrokesKafkaConfig, "ladbrokesKafkaProperties", ladbrokesKafkaProperties);
    ReflectionTestUtils.setField(ladbrokesKafkaConfig, "ladsPartitions", 1);
    ReflectionTestUtils.setField(ladbrokesKafkaConfig, "replicaFactor", (short) 1);
    ReflectionTestUtils.setField(
        ladbrokesKafkaConfig, "leaderboardContestTopic", "LOCAL-LDRBRD-leaderboard-contest");
    ReflectionTestUtils.setField(ladbrokesKafkaConfig, "ladsTimelineTopic", "timeline");
  }

  @Test
  public void testKafkaAdmin() {
    KafkaAdmin kafkaAdmin = ladbrokesKafkaConfig.admin();
    Assert.assertNotNull(kafkaAdmin);
  }

  @Test
  public void testAdminClient() {
    AdminClient adminClient = ladbrokesKafkaConfig.adminClient();
    Assert.assertNotNull(adminClient);
  }

  @Test
  public void testProducerFactory() {
    ProducerFactory<String, String> ladbrokesProducerFactory =
        ladbrokesKafkaConfig.ladbrokesProducerFactory();
    Assert.assertNotNull(ladbrokesProducerFactory);
  }

  @Test
  public void testcontestTopic() {
    NewTopic topic = ladbrokesKafkaConfig.contestTopic();
    Assert.assertNotNull(topic);
  }

  @Test
  public void testkafkaTemplateLeaderboardContest() {
    KafkaTemplate<String, String> kafkaConfigTemplate =
        ladbrokesKafkaConfig.ladbrokesKafkaTemplate();
    Assert.assertNotNull(kafkaConfigTemplate);
  }

  @Test
  public void testleaderboardPromoTopic() {
    NewTopic leaderboardPromoTopic = ladbrokesKafkaConfig.leaderboardPromoTopic();
    Assert.assertNotNull(leaderboardPromoTopic);
  }

  @Test
  public void testpromoLeaderboardProducerFactory() {
    ProducerFactory<String, PromoMessageDto> factory =
        ladbrokesKafkaConfig.promoLeaderboardProducerFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  public void testpromoLeaderboardKafkaTemplate() {
    KafkaTemplate<String, PromoMessageDto> kafkaConfigTemplate =
        ladbrokesKafkaConfig.promoLeaderboardKafkaTemplate();
    Assert.assertNotNull(kafkaConfigTemplate);
  }

  @Test
  public void testTimelineTopic() {
    NewTopic timeline = ladbrokesKafkaConfig.ladsTimelineTopic();
    Assertions.assertNotNull(timeline);
  }

  @Test
  public void testLadsTimelineProducerFactory() {
    ProducerFactory<String, TimelineMessageDto> producerFactory =
        ladbrokesKafkaConfig.ladsTimelineProducerFactory();
    Assertions.assertNotNull(producerFactory);
  }

  @Test
  public void testLadsTimelineConfigProducerFactory() {
    ProducerFactory<String, TimelineConfigDto> producerFactory =
        ladbrokesKafkaConfig.ladsTimelineProducerConfigFactory();
    Assertions.assertNotNull(producerFactory);
  }

  @Test
  public void testLadsTimelineKafkaTemplate() {
    KafkaTemplate<String, TimelineMessageDto> kafkaTemplate =
        ladbrokesKafkaConfig.ladsTimelineKafkaTemplate();
    Assertions.assertNotNull(kafkaTemplate);
  }

  @Test
  public void testLadsTimelineConfigTemplate() {
    KafkaTemplate<String, TimelineConfigDto> kafkaTemplate =
        ladbrokesKafkaConfig.ladsTimelineKafkaConfigTemplate();
    Assertions.assertNotNull(kafkaTemplate);
  }
}
