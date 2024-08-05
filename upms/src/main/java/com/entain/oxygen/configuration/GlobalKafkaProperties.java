package com.entain.oxygen.configuration;

import java.util.Map;
import lombok.Data;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "rtms")
@Data
public class GlobalKafkaProperties {
  private KafkaProperties kafka;
  private Map<String, TopicProperties> topics;

  @Data
  static class TopicProperties {
    private int partitions;
    private short replica;
  }
}
