package com.ladbrokescoral.oxygen.betpackmp.configuration;

import com.ladbrokescoral.oxygen.betpackmp.kafka.filter.BetPackDFPafKafkaConsumerFilter;
import com.ladbrokescoral.oxygen.betpackmp.model.PafExtractorPromotion;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;
import org.springframework.kafka.support.serializer.JsonDeserializer;

@Configuration
@EnableKafka
@EnableConfigurationProperties
public class DfKafkaConfig {

  @Bean
  public KafkaListenerContainerFactory<
          ConcurrentMessageListenerContainer<String, PafExtractorPromotion>>
      filteredKafkaPafContainerFactory(
          DfKafkaProperties dfKafkaProperties,
          @Value("${df.kafka.listenersConcurrency}") Integer listenersConcurrency,
          BetPackDFPafKafkaConsumerFilter betPackDFPafKafkaConsumerFilter) {

    ConcurrentKafkaListenerContainerFactory<String, PafExtractorPromotion> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConcurrency(listenersConcurrency);

    DefaultKafkaConsumerFactory<String, PafExtractorPromotion> consumerFactory =
        new DefaultKafkaConsumerFactory<>(
            dfKafkaProperties.getKafka().getConsumer().buildProperties());
    consumerFactory.setKeyDeserializer(new StringDeserializer());
    consumerFactory.setValueDeserializer(new JsonDeserializer<>(PafExtractorPromotion.class));
    factory.setConsumerFactory(consumerFactory);
    factory.setRecordFilterStrategy(betPackDFPafKafkaConsumerFilter);
    return factory;
  }
}
