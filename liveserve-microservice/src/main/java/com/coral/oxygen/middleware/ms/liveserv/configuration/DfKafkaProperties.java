package com.coral.oxygen.middleware.ms.liveserv.configuration;

import java.util.Map;
import lombok.Data;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "df")
@Data
public class DfKafkaProperties {
  private KafkaProperties kafka;
  private Map<String, TopicProperties> topics;

  @Data
  static class TopicProperties {
    private int partitions;
    private short replica;
  }
}