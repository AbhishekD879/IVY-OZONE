package com.ladbrokescoral.oxygen.configuration;

import com.ladbrokescoral.oxygen.model.FreebetOffer;
import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;
import org.springframework.kafka.support.serializer.JsonDeserializer;

@ConditionalOnProperty(prefix = "bet-bundle", value = "enabled", havingValue = "true")
@ComponentScan("com.ladbrokescoral.oxygen")
@Configuration
public class BetPackKafkaConsumerConfig {

  @Value("${spring.kafka.bootstrap-servers}")
  String bootstrapServers;

  @Value("${kafka.live.update.consumers.count}")
  Integer kafkaConsumerCount;

  @Value("${topic.bet-pack-live-updates.group-id}")
  String betPackGroupId;

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, FreebetOffer>>
      kafkaBetPacksListenerContainerFactory() {
    ConcurrentKafkaListenerContainerFactory<String, FreebetOffer> factory =
        new ConcurrentKafkaListenerContainerFactory<>();

    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
    props.put(ConsumerConfig.GROUP_ID_CONFIG, betPackGroupId);
    props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");

    DefaultKafkaConsumerFactory<String, FreebetOffer> consumerFactory =
        new DefaultKafkaConsumerFactory<>(
            props, stringKeyDeserializer(), betPackJsonValueDeserializer());

    factory.setConsumerFactory(consumerFactory);
    factory.setConcurrency(kafkaConsumerCount);
    return factory;
  }

  @Bean
  public Deserializer<String> stringKeyDeserializer() {
    return new StringDeserializer();
  }

  @Bean
  public Deserializer<FreebetOffer> betPackJsonValueDeserializer() {
    return new JsonDeserializer<>(FreebetOffer.class, false);
  }
}
