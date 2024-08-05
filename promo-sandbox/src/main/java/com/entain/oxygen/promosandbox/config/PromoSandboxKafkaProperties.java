package com.entain.oxygen.promosandbox.config;

import lombok.Data;
import org.springframework.boot.autoconfigure.kafka.KafkaProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "promosandbox")
@Data
public class PromoSandboxKafkaProperties {
  private KafkaProperties kafka;
}
