package com.ladbrokescoral.oxygen.configuration;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.listener.ConcurrentMessageListenerContainer;

@EnableKafka
@ComponentScan("com.ladbrokescoral.oxygen")
@Configuration
public class KafkaConsumerConfig {

  private static final String YYYY_MM_DD_HH_MM_SS = "yyyy-MM-dd_HH:mm:ss";

  @Value("${spring.kafka.bootstrap-servers}")
  String bootstrapServers;

  @Value("${kafka.live.update.consumers.count}")
  Integer kafkaConsumerCount;

  @Bean
  public Map<String, Object> consumerConfigs() {
    Map<String, Object> props = new HashMap<>();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    String date =
        new SimpleDateFormat(YYYY_MM_DD_HH_MM_SS).format(Calendar.getInstance().getTime());
    props.put(
        ConsumerConfig.GROUP_ID_CONFIG,
        String.format("LSRV-PUB-%s-%s", UUID.randomUUID().toString(), date));
    props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
    return props;
  }

  @Bean
  public ConsumerFactory consumerFactory() {
    return new DefaultKafkaConsumerFactory<>(consumerConfigs());
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      kafkaLiveupdatesListenerContainerFactory() {
    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    factory.setConsumerFactory(consumerFactory());
    factory.setConcurrency(kafkaConsumerCount);
    return factory;
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      kafkaScoreboardsListenerContainerFactory() {
    return createKafkaListenerContainer();
  }

  @Bean
  public KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      kafkaLeaderboardUpdatesListenerContainerFactory() {
    return createKafkaListenerContainer();
  }

  private KafkaListenerContainerFactory<ConcurrentMessageListenerContainer<String, String>>
      createKafkaListenerContainer() {
    ConcurrentKafkaListenerContainerFactory<String, String> factory =
        new ConcurrentKafkaListenerContainerFactory<>();
    DefaultKafkaConsumerFactory<String, String> consumerFactory =
        new DefaultKafkaConsumerFactory<>(consumerConfigs());

    consumerFactory.setKeyDeserializer(new StringDeserializer());
    consumerFactory.setValueDeserializer(new StringDeserializer());
    factory.setConsumerFactory(consumerFactory);
    factory.setConcurrency(kafkaConsumerCount);
    return factory;
  }
}
