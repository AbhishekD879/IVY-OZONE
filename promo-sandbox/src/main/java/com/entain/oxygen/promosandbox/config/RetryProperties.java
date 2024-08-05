package com.entain.oxygen.promosandbox.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties("retry")
public class RetryProperties {
  private int retryMaxAttempts;
}
