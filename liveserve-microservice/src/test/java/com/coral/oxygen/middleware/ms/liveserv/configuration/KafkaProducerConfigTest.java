package com.coral.oxygen.middleware.ms.liveserv.configuration;

import org.apache.kafka.clients.admin.NewTopic;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
class KafkaProducerConfigTest {

  private KafkaProducerConfig kafkaProducerConfig;
  private String kafkaBrokers = "localhost:9092";
  private String liveUpdatesTopicName = "live.update.1";
  private String scoreboardsTopic = "test.scoreboard.1";
  protected Integer defaultNumPartitions = 6;
  protected short replicaFactor = 1;
  private String incidentsTopic = "test.incidnets.1";

  @Test
  void incidentsTopic() {
    kafkaProducerConfig =
        new KafkaProducerConfig(
            kafkaBrokers,
            liveUpdatesTopicName,
            scoreboardsTopic,
            defaultNumPartitions,
            replicaFactor,
            incidentsTopic);

    NewTopic topic = kafkaProducerConfig.incidentsTopic();
    Assert.assertNotNull(topic);
  }
}
