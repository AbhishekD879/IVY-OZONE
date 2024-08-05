package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.ladbrokescoral.oxygen.betpackmp.model.PafExtractorPromotion;
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
class DfKafkaConfigTest implements WithAssertions {

  @InjectMocks private DfKafkaConfig dfKafkaConfig;

  @BeforeEach
  public void init() {
    dfKafkaConfig = new DfKafkaConfig();
  }

  @Test
  void filteredKafkaPafContainerFactory() {
    KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, PafExtractorPromotion>>
        result = dfKafkaConfig.filteredKafkaPafContainerFactory(getDfKafkaProperties(), 67, null);
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
