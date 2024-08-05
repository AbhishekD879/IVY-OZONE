package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.api.client.entity.request.CashoutRequest;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.updates.BetDetailRequestCtx;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.RoundRobinAssignor;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import reactor.kafka.receiver.ReceiverOptions;

@Configuration
public class ReactiveKafkaConsumerConfig {

  @Value("${internal.topics.bet-detail-requests.groupId}")
  private String betDetailTopicGroupId;

  @Value("${internal.topics.cashout-offer-requests.groupId}")
  private String cashoutOfferTopicGroupId;

  @Value("${internal.topics.bet-updates.groupId}-${random.uuid}")
  private String betUpdatesGroupId;

  @Value("${internal.topics.bet-updates-errors.groupId}-${random.uuid}")
  private String betUpdatesErrorGroupId;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  /**
   * Consumer configuration for bet-detail-requests topic
   *
   * @param kafkaProperties
   * @return
   */
  @Bean
  public Map<String, Object> kafkaConsumerConfiguration(InternalKafkaProperties kafkaProperties) {
    Map<String, Object> configs = new HashMap<>(kafkaProperties.getKafka().buildAdminProperties());
    ASYNC_LOGGER.info(
        "SSL truststore path ::{}",
        kafkaProperties.getKafka().getConsumer().getSsl().getTrustStoreLocation());
    ASYNC_LOGGER.info(
        "SSL keystore path ::{}",
        kafkaProperties.getKafka().getConsumer().getSsl().getKeyStoreLocation());
    ASYNC_LOGGER.info("Bootstrap Servers ::{}", kafkaProperties.getKafka().getBootstrapServers());
    configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, betDetailTopicGroupId);
    configs.put(JsonDeserializer.TRUSTED_PACKAGES, "*");
    return configs;
  }

  @Bean
  public ReceiverOptions<String, BetDetailRequestCtx> kafkaReceiverOptions(
      InternalKafkaProperties kafkaProperties) {
    ReceiverOptions<String, BetDetailRequestCtx> basicReceiverOptions =
        ReceiverOptions.create(kafkaConsumerConfiguration(kafkaProperties));
    return basicReceiverOptions
        .subscription(Collections.singleton("bet-detail-requests"))
        .withKeyDeserializer(new StringDeserializer())
        .withValueDeserializer(new JsonDeserializer<>(BetDetailRequestCtx.class, false));
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, BetDetailRequestCtx> reactiveKafkaConsumerTemplate(
      ReceiverOptions<String, BetDetailRequestCtx> kafkaReceiverOptions) {
    return new ReactiveKafkaConsumerTemplate<>(kafkaReceiverOptions);
  }
  /**
   * Consumer configuration for cashout-offer-requests topic
   *
   * @param kafkaProperties
   * @return
   */
  @Bean
  public Map<String, Object> cashoutOfferkafkaConsumerConfiguration(
      InternalKafkaProperties kafkaProperties) {
    Map<String, Object> configs = new HashMap<>(kafkaProperties.getKafka().buildAdminProperties());
    configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, cashoutOfferTopicGroupId);
    configs.put(JsonDeserializer.TRUSTED_PACKAGES, "*");
    return configs;
  }

  @Bean
  public ReceiverOptions<String, CashoutRequest> betDetailKafkaReceiverOptions(
      InternalKafkaProperties kafkaProperties) {
    ReceiverOptions<String, CashoutRequest> basicReceiverOptions =
        ReceiverOptions.create(cashoutOfferkafkaConsumerConfiguration(kafkaProperties));
    return basicReceiverOptions
        .subscription(Collections.singleton("cashout-offer-requests"))
        .withKeyDeserializer(new StringDeserializer())
        .withValueDeserializer(new JsonDeserializer<>(CashoutRequest.class, false));
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, CashoutRequest>
      betDetailreactiveKafkaConsumerTemplate(
          ReceiverOptions<String, CashoutRequest> betDetailKafkaReceiverOptions) {
    return new ReactiveKafkaConsumerTemplate<>(betDetailKafkaReceiverOptions);
  }

  /**
   * Consumer configuration for bet-updates topic
   *
   * @param kafkaProperties
   * @return
   */
  @Bean
  public Map<String, Object> betUpdatesKafkaConsumerConfiguration(
      InternalKafkaProperties kafkaProperties) {
    Map<String, Object> configs = new HashMap<>(kafkaProperties.getKafka().buildAdminProperties());
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, betUpdatesGroupId);
    configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(
        ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, RoundRobinAssignor.class.getName());
    configs.put(JsonDeserializer.TRUSTED_PACKAGES, "*");
    return configs;
  }

  @Bean
  public ReceiverOptions<String, UpdateDto> betUpdatesKafkaReceiverOptions(
      InternalKafkaProperties kafkaProperties) {
    ReceiverOptions<String, UpdateDto> basicReceiverOptions =
        ReceiverOptions.create(betUpdatesKafkaConsumerConfiguration(kafkaProperties));
    return basicReceiverOptions
        .subscription(Collections.singleton("bet-updates"))
        .withKeyDeserializer(new StringDeserializer())
        .withValueDeserializer(new JsonDeserializer<>(UpdateDto.class, false));
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, UpdateDto> betUpdatesReactiveKafkaConsumerTemplate(
      ReceiverOptions<String, UpdateDto> betUpdatesKafkaReceiverOptions) {
    return new ReactiveKafkaConsumerTemplate<>(betUpdatesKafkaReceiverOptions);
  }

  /**
   * Consumer configuration for bet-updates-error topic
   *
   * @param kafkaProperties
   * @return
   */
  @Bean
  public Map<String, Object> betUpdatesErrorKafkaConsumerConfiguration(
      InternalKafkaProperties kafkaProperties) {
    Map<String, Object> configs = new HashMap<>(kafkaProperties.getKafka().buildAdminProperties());
    configs.put(ConsumerConfig.GROUP_ID_CONFIG, betUpdatesErrorGroupId);
    configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(
        ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, RoundRobinAssignor.class.getName());
    configs.put(JsonDeserializer.TRUSTED_PACKAGES, "*");
    return configs;
  }

  @Bean
  public ReceiverOptions<String, Throwable> betUpdatesErrorKafkaReceiverOptions(
      InternalKafkaProperties kafkaProperties) {
    ReceiverOptions<String, Throwable> basicReceiverOptions =
        ReceiverOptions.create(betUpdatesErrorKafkaConsumerConfiguration(kafkaProperties));
    return basicReceiverOptions
        .subscription(Collections.singleton("bet-updates-errors"))
        .withKeyDeserializer(new StringDeserializer())
        .withValueDeserializer(new JsonDeserializer<>(Throwable.class, false));
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, Throwable>
      betUpdatesErrorReactiveKafkaConsumerTemplate(
          ReceiverOptions<String, Throwable> betUpdatesErrorKafkaReceiverOptions) {
    return new ReactiveKafkaConsumerTemplate<>(betUpdatesErrorKafkaReceiverOptions);
  }
}
