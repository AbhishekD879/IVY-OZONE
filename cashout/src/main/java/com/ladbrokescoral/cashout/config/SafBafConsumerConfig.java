package com.ladbrokescoral.cashout.config;

import com.ladbrokescoral.cashout.util.Message;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.reactive.ReactiveKafkaConsumerTemplate;
import org.springframework.util.StringUtils;
import reactor.kafka.receiver.ReceiverOptions;

@Configuration
public class SafBafConsumerConfig {

  @Value("${cashout.build-number}")
  private String buildNumber;

  @Value("${app.df.topic.saf}")
  private String safTopic;

  @Value("${app.df.topic.baf}")
  private String bafTopic;

  @Value("${random.uuid}")
  private String uuid;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private Message message;

  @Bean
  public ReceiverOptions<String, String> basicReceiverOptions(DfKafkaProperties dfKafkaProperties) {
    Map<String, Object> configs =
        new HashMap<>(dfKafkaProperties.getKafka().buildConsumerProperties());
    ASYNC_LOGGER.info(
        "SSL truststore path ::{}",
        dfKafkaProperties.getKafka().getConsumer().getSsl().getTrustStoreLocation());
    ASYNC_LOGGER.info(
        "SSL keystore path ::{}",
        dfKafkaProperties.getKafka().getConsumer().getSsl().getKeyStoreLocation());
    ASYNC_LOGGER.info(
        "DF Bootstrap Servers ::{}", dfKafkaProperties.getKafka().getBootstrapServers());
    configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
    return ReceiverOptions.create(configs);
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, String> bafUpdatesListenerTemplate(
      ReceiverOptions<String, String> basicReceiverOptions) {
    message = new Message();
    String bafConsumerGroup = buildGroupId(bafTopic, buildNumber, uuid);
    message.setMessage(bafConsumerGroup);
    ASYNC_LOGGER.error("Listening with the consumer group {}", message);
    ReceiverOptions<String, String> receiverOptions =
        basicReceiverOptions.consumerProperty(ConsumerConfig.GROUP_ID_CONFIG, bafConsumerGroup);
    receiverOptions = receiverOptions.subscription(Collections.singletonList(bafTopic));
    return new ReactiveKafkaConsumerTemplate<>(receiverOptions);
  }

  @Bean
  public ReactiveKafkaConsumerTemplate<String, String> safUpdatesListenerTemplate(
      ReceiverOptions<String, String> basicReceiverOptions) {
    message = new Message();
    String safConsumerGroup = buildGroupId(safTopic, buildNumber, uuid);
    message.setMessage(safConsumerGroup);
    ASYNC_LOGGER.error("Listening with the consumer group {}", message);
    ReceiverOptions<String, String> receiverOptions =
        basicReceiverOptions.consumerProperty(ConsumerConfig.GROUP_ID_CONFIG, safConsumerGroup);
    receiverOptions = receiverOptions.subscription(Collections.singletonList(safTopic));
    return new ReactiveKafkaConsumerTemplate<>(receiverOptions);
  }

  public String buildGroupId(String groupId, String buildId, String uuid) {
    if (StringUtils.hasLength(uuid)) uuid = "-" + uuid;
    return groupId
        + "-"
        + DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm")
            .withZone(ZoneId.systemDefault())
            .format(Instant.now())
        + "-"
        + buildId
        + uuid;
  }
}
