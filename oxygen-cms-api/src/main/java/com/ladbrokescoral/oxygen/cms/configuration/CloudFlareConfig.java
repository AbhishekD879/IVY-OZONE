package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@Data
@ConfigurationProperties(prefix = "cloudflare")
public class CloudFlareConfig {
  private String endpoint;
  private String token;
}
