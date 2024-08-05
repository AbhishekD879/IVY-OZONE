package com.coral.oxygen.middleware.in_play.service.config;

import org.junit.Assert;
import org.junit.Test;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;

public class DfKafkaConfigTest {

  private DfKafkaConfig dfKafkaConfig;
  private DfKafkaProperties dfKafkaProperties;

  @Test
  public void DfKafkaConfigurationTest() {
    dfKafkaProperties = new DfKafkaProperties();
    KafkaProperties kafkaProperties = new KafkaProperties();
    kafkaProperties.buildConsumerProperties().put("abc", Object.class);
    dfKafkaConfig = new DfKafkaConfig();
    dfKafkaProperties.setKafka(kafkaProperties);
    dfKafkaConfig.filteredKafkaScoreBoardsContainerFactory(dfKafkaProperties, 10);
    Assert.assertNotNull(kafkaProperties);
  }
}
