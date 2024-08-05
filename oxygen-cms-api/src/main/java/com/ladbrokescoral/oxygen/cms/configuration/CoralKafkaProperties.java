package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Data;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "coral")
@Data
public class CoralKafkaProperties {
  private KafkaProperties kafka;
}
