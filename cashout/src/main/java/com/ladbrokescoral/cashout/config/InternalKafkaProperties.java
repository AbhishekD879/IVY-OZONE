package com.ladbrokescoral.cashout.config;

import java.time.Duration;
import java.util.Map;
import lombok.Data;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "internal")
@Data
public class InternalKafkaProperties {

  private KafkaProperties kafka;
  private Map<String, TopicProperties> topics;
  private int listenersConcurrency = 10;

  /** Retention policy for all internal topics of cashout microservice (5 minutes default) */
  private Duration retention = Duration.ofMinutes(5);

  @Data
  static class TopicProperties {
    private int partitions;
    private short replica;
  }
}
