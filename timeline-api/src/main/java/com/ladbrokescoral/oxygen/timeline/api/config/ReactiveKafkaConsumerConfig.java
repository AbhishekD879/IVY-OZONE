package com.ladbrokescoral.oxygen.timeline.api.config;

import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import java.util.Collections;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import reactor.kafka.receiver.ReceiverOptions;

@Configuration
public class ReactiveKafkaConsumerConfig {

  @Bean
  public ReceiverOptions<String, Message> kafkaReceiverOptions(
      @Value(value = "${spring.kafka.topic.main}") String timelineTopic,
      KafkaProperties kafkaProperties) {
    ReceiverOptions<String, Message> basicReceiverOptions =
        ReceiverOptions.create(kafkaProperties.buildConsumerProperties());
    return basicReceiverOptions.subscription(Collections.singletonList(timelineTopic));
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, Message> reactiveKafkaConsumerTemplate(
      ReceiverOptions<String, Message> kafkaReceiverOptions) {
    return new ReactiveKafkaConsumerTemplate<String, Message>(kafkaReceiverOptions);
  }
}
