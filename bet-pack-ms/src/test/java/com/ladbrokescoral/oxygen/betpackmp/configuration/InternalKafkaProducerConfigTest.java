package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.coral.bpp.api.model.bet.api.response.freebetoffer.FreebetOffer;
import java.util.Map;
import org.apache.kafka.clients.admin.AdminClient;
import org.apache.kafka.clients.admin.NewTopic;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaAdmin;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;

@ExtendWith(MockitoExtension.class)
class InternalKafkaProducerConfigTest implements WithAssertions {

  private final String kafkaBrokers = "localhost:9092";
  private final String betPackUpdatesTopicName = "bet-pack-updates-topic";
  private Integer defaultNumPartitions = 1;
  private short replicaFactor = 1;

  @InjectMocks
  private InternalKafkaProducerConfig kafkaProducerConfig =
      new InternalKafkaProducerConfig(
          kafkaBrokers, betPackUpdatesTopicName, defaultNumPartitions, replicaFactor);

  @Test
  void liveUpdatesTopic() {
    NewTopic topic = kafkaProducerConfig.liveUpdatesTopic();
    Assertions.assertNotNull(topic);
  }

  @Test
  void producerFactory() {
    ProducerFactory<String, FreebetOffer> result = kafkaProducerConfig.producerFactory();
    Assertions.assertNotNull(result);
  }

  @Test
  void admin() {
    KafkaAdmin result = kafkaProducerConfig.admin();
    Assertions.assertNotNull(result);
  }

  @Test
  void adminClient() {
    AdminClient result = kafkaProducerConfig.adminClient();
    Assertions.assertNotNull(result);
  }

  @Test
  void producerConfigs() {
    Map<String, Object> result = kafkaProducerConfig.producerConfigs();
    Assertions.assertNotNull(result);
  }

  @Test
  void kafkaTemplate() {
    KafkaTemplate<String, FreebetOffer> result = kafkaProducerConfig.kafkaTemplate();
    Assertions.assertNotNull(result);
  }
}
