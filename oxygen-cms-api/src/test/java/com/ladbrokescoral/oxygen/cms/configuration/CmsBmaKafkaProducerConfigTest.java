package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.dto.PromoMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineMessageDto;
import java.util.List;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.assertj.core.api.WithAssertions;
import org.junit.Assert;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class CmsBmaKafkaProducerConfigTest implements WithAssertions {

  @InjectMocks private CmsBmaKafkaProducerConfig cmsBmaKafkaProducerConfig;

  @BeforeEach
  void setUp() {
    CoralKafkaProperties coralKafkaProperties = new CoralKafkaProperties();
    coralKafkaProperties.setKafka(new KafkaProperties());
    cmsBmaKafkaProducerConfig = new CmsBmaKafkaProducerConfig(coralKafkaProperties);
    ReflectionTestUtils.setField(
        cmsBmaKafkaProducerConfig, "coralKafkaProperties", coralKafkaProperties);
    ReflectionTestUtils.setField(cmsBmaKafkaProducerConfig, "coralPartitions", 1);
    ReflectionTestUtils.setField(cmsBmaKafkaProducerConfig, "coralReplicaFactor", (short) 1);
    ReflectionTestUtils.setField(
        cmsBmaKafkaProducerConfig, "coralActiveBetPackTopic", "coral-active-bet-packs-topic");
    ReflectionTestUtils.setField(cmsBmaKafkaProducerConfig, "coralTimelineTopic", "timeline");
  }

  @Test
  void coralBetPackProducerFactory() {
    ProducerFactory<String, List<String>> producerFactory =
        cmsBmaKafkaProducerConfig.coralBetPackProducerFactory();
    Assertions.assertNotNull(producerFactory);
  }

  @Test
  void coralBetPackKafkaTemplate() {
    KafkaTemplate<String, List<String>> kafkaTemplate =
        cmsBmaKafkaProducerConfig.coralBetPackKafkaTemplate();
    Assertions.assertNotNull(kafkaTemplate);
  }

  @Test
  void testKafkaAdmin() {
    KafkaAdmin kafkaAdmin = cmsBmaKafkaProducerConfig.admin();
    Assert.assertNotNull(kafkaAdmin);
  }

  @Test
  void testKafkaAdminClient() {
    AdminClient adminClient = cmsBmaKafkaProducerConfig.adminClient();
    Assert.assertNotNull(adminClient);
  }

  @Test
  void testActiveBetPackTopic() {
    NewTopic activeBetPackTopic = cmsBmaKafkaProducerConfig.activeBetPackTopic();
    Assert.assertNotNull(activeBetPackTopic);
  }

  @Test
  void testCoralTimelineTopic() {
    NewTopic coralTimelineTopic = cmsBmaKafkaProducerConfig.coralTimelineTopic();
    Assert.assertNotNull(coralTimelineTopic);
  }

  @Test
  void testProducerFactory() {
    ProducerFactory<String, TimelineMessageDto> factory =
        cmsBmaKafkaProducerConfig.producerFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  void testProducerConfigFactory() {
    ProducerFactory<String, TimelineConfigDto> factory =
        cmsBmaKafkaProducerConfig.producerConfigFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  void testKafkaTemplate() {
    KafkaTemplate<String, TimelineMessageDto> kafkaTemplate =
        cmsBmaKafkaProducerConfig.kafkaTemplate();
    Assert.assertNotNull(kafkaTemplate);
  }

  @Test
  void testKafkaConfigTemplate() {
    KafkaTemplate<String, TimelineConfigDto> kafkaConfigTemplate =
        cmsBmaKafkaProducerConfig.kafkaConfigTemplate();
    Assert.assertNotNull(kafkaConfigTemplate);
  }

  @Test
  void testleaderboardPromoCoralTopic() {
    NewTopic leaderboardPromoCoralTopic = cmsBmaKafkaProducerConfig.leaderboardPromoCoralTopic();
    Assert.assertNotNull(leaderboardPromoCoralTopic);
  }

  @Test
  void promoLeaderboardCoralProducerFactory() {
    ProducerFactory<String, PromoMessageDto> factory =
        cmsBmaKafkaProducerConfig.promoLeaderboardCoralProducerFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  void testpromoLeaderboardCoralKafkaTemplate() {
    KafkaTemplate<String, PromoMessageDto> kafkaConfigTemplate =
        cmsBmaKafkaProducerConfig.promoLeaderboardCoralKafkaTemplate();
    Assert.assertNotNull(kafkaConfigTemplate);
  }

  @Test
  void testCMSPushProducerFactory() {
    ProducerFactory<String, String> factory = cmsBmaKafkaProducerConfig.coralProducerFactory();
    Assert.assertNotNull(factory);
  }

  @Test
  void testCoralKafkaTemplate() {
    KafkaTemplate<String, String> coralKafkaTemplate =
        cmsBmaKafkaProducerConfig.coralKafkaTemplate();
    Assert.assertNotNull(coralKafkaTemplate);
  }
}
