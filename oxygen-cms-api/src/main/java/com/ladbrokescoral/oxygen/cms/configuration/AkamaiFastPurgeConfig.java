package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@Data
@ConfigurationProperties(prefix = "fastpurge")
public class AkamaiFastPurgeConfig {
  private String scheme;
  private String host;
  private String invalidateCpCodePath;
  private String invalidateUrlPath;
  private String clientSecret;
  private String accessToken;
  private String clientToken;
  private String[] cpCode;
}
