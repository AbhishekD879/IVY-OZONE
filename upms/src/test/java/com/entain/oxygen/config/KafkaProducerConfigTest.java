package com.entain.oxygen.config;

import com.entain.oxygen.configuration.GlobalKafkaProducerConfig;
import com.entain.oxygen.configuration.GlobalKafkaProperties;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class KafkaProducerConfigTest implements WithAssertions {

  private final String kafkaBrokers = "localhost:9092";
  private final String rtmsUpdateTopic = "UPMS_RTMS";
  private Integer defaultNumPartitions = 1;
  private short replicaFactor = 1;

  private GlobalKafkaProducerConfig kafkaProducerConfig;

  private GlobalKafkaProperties globalKafkaProperties;

  @BeforeAll
  void init() throws NoSuchFieldException, IllegalAccessException {
    globalKafkaProperties = new GlobalKafkaProperties();
    globalKafkaProperties.setKafka(new KafkaProperties());
    kafkaProducerConfig = new GlobalKafkaProducerConfig();
    ReflectionTestUtils.setField(
        kafkaProducerConfig, "globalKafkaProperties", globalKafkaProperties);
  }

  @Test
  void testKafkaTemplate() {
    KafkaTemplate<String, String> result = kafkaProducerConfig.globalKafkaTemplate();
    Assertions.assertNotNull(result);
  }
}
