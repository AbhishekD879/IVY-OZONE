package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Data;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "ladbrokes")
@Data
public class LadbrokesKafkaProperties {
  private KafkaProperties kafka;
}
