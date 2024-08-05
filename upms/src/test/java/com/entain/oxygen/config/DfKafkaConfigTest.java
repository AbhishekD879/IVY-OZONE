package com.entain.oxygen.config;

import com.entain.oxygen.configuration.DfKafkaProperties;
import com.entain.oxygen.configuration.KafkaConsumerConfig;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@ExtendWith(MockitoExtension.class)
class KafkaConsumerConfigTest implements WithAssertions {

  @InjectMocks private KafkaConsumerConfig dfKafkaConfig;

  @BeforeEach
  public void init() {
    dfKafkaConfig = new KafkaConsumerConfig();
  }

  @Test
  void filteredKafkaContainerFactory() {
    KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>> result =
        dfKafkaConfig.filteredKafkaContainerFactory(getDfKafkaProperties(), 67);
    Assertions.assertNotNull(result);
  }

  public DfKafkaProperties getDfKafkaProperties() {
    DfKafkaProperties kafkaProperties = new DfKafkaProperties();
    KafkaProperties kafka = new KafkaProperties();
    kafkaProperties.setKafka(kafka);
    kafkaProperties.getKafka().getConsumer().buildProperties();
    return kafkaProperties;
  }
}
